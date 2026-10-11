import uuid
import time
import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.realtime import VideoUploadSession
from app.schemas.video_analysis import VideoAnalysisResponse
from app.services.motion_analysis import MotionAnalysisService
from app.services.mechanism_inference import MechanismInferenceService
from app.services.realtime_motion_processor import RealtimeMotionProcessor
from app.services.system_health import health_monitor
from app.utils.audit_trail import AuditTrail
import os
import cv2
import numpy as np

router = APIRouter(prefix="/videos", tags=["videos"])
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_video(
    device_name: str = Form("salvaged mechanism"),
    notes: str | None = Form(None),
    motion_hint: str | None = Form(None),
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
):
    """Upload video file and initiate analysis session."""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video file is required"
        )
    
    # Validate file type
    valid_extensions = {"mp4", "avi", "mov", "webm", "mkv"}
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in valid_extensions:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported video format: {file_ext}. Supported: {', '.join(valid_extensions)}"
        )
    
    # Create upload directory
    os.makedirs("./data/uploads", exist_ok=True)
    
    # Generate session ID
    session_id = str(uuid.uuid4())
    upload_path = f"./data/uploads/{session_id}_{file.filename}"
    
    # Save file
    contents = await file.read()
    file_size = len(contents)
    
    with open(upload_path, "wb") as f:
        f.write(contents)
    
    # Create session record
    session = VideoUploadSession(
        session_id=session_id,
        device_name=device_name,
        input_notes=notes,
        motion_hint=motion_hint,
        video_filename=file.filename,
        video_size_bytes=file_size,
        upload_status="uploaded",
        analysis_status="queued",
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # Queue background analysis
    if background_tasks:
        background_tasks.add_task(
            process_video_analysis,
            session_id=session_id,
            upload_path=upload_path,
            device_name=device_name,
        )
    
    logger.info(f"Video uploaded: {session_id} ({file_size} bytes)")
    
    return {
        "session_id": session_id,
        "filename": file.filename,
        "file_size_bytes": file_size,
        "status": "uploaded",
        "message": "Analysis queued for processing",
    }

@router.get("/status/{session_id}")
def get_analysis_status(session_id: str, db: Session = Depends(get_db)):
    """Get real-time analysis status for a session."""
    session = db.query(VideoUploadSession).filter(
        VideoUploadSession.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return {
        "session_id": session_id,
        "device_name": session.device_name,
        "upload_status": session.upload_status,
        "analysis_status": session.analysis_status,
        "progress_percent": session.progress_percent,
        "processing_time_ms": session.processing_time_ms,
        "error_message": session.error_message,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
    }

@router.get("/result/{session_id}", response_model=VideoAnalysisResponse)
def get_analysis_result(session_id: str, db: Session = Depends(get_db)):
    """Get completed analysis result."""
    session = db.query(VideoUploadSession).filter(
        VideoUploadSession.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if session.analysis_status != "completed":
        raise HTTPException(
            status_code=status.HTTP_425_TOO_EARLY,
            detail=f"Analysis not yet complete: {session.analysis_status}"
        )
    
    if not session.result_json:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analysis result not available"
        )
    
    import json
    result_data = json.loads(session.result_json)
    return VideoAnalysisResponse(**result_data)

@router.post("/analyze", response_model=VideoAnalysisResponse)
async def analyze_video_sync(
    device_name: str = Form("salvaged mechanism"),
    notes: str | None = Form(None),
    motion_hint: str | None = Form(None),
    frame_count: int = Form(30),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Synchronous video analysis endpoint."""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video file is required"
        )
    
    os.makedirs("./data/uploads", exist_ok=True)
    session_id = str(uuid.uuid4())
    upload_path = f"./data/uploads/{session_id}_{file.filename}"
    
    contents = await file.read()
    with open(upload_path, "wb") as f:
        f.write(contents)
    
    try:
        start_time = time.time()
        
        # Extract motion profile
        motion_service = MotionAnalysisService()
        motion_profile = motion_service.extract_motion_features(upload_path, max_frames=frame_count)
        
        # Infer mechanism
        inference_service = MechanismInferenceService()
        inference = inference_service.infer(device_name, motion_profile, notes, motion_hint)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Create response
        response = VideoAnalysisResponse(
            device_name=device_name,
            mechanism_summary=inference["mechanism_summary"],
            motion_profile={
                "dominant_motion": motion_profile.get("dominant_motion", "unknown"),
                "cycle_estimate": motion_profile.get("cycle_estimate"),
                "confidence": float(motion_profile.get("confidence", 0.0)),
                "sampled_frames": int(motion_profile.get("sampled_frames", 0)),
                "analysis_method": motion_profile.get("method"),
            },
            likely_faults=inference["likely_faults"],
            repair_steps=inference["repair_steps"],
            repurpose_options=inference["repurpose_options"],
            safety_warnings=inference["safety_warnings"],
            confidence=float(inference["confidence"]),
        )
        
        health_monitor.completed_sessions += 1
        health_monitor.record_metric("analysis_completed", 1, tags="status=success")
        health_monitor.record_metric("analysis_time_ms", processing_time, unit="ms")
        
        logger.info(f"Analysis completed: {session_id} in {processing_time}ms")
        
        return response
        
    except Exception as e:
        health_monitor.record_error(str(e))
        logger.error(f"Analysis failed for {session_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

async def process_video_analysis(session_id: str, upload_path: str, device_name: str):
    """Background task for video analysis processing."""
    db = None
    try:
        from app.core.database import SessionLocal
        db = SessionLocal()
        
        session_record = db.query(VideoUploadSession).filter(
            VideoUploadSession.session_id == session_id
        ).first()
        
        if not session_record:
            logger.error(f"Session not found: {session_id}")
            return
        
        start_time = time.time()
        health_monitor.active_sessions += 1
        
        # Process video
        session_record.analysis_status = "processing"
        db.commit()
        
        motion_service = MotionAnalysisService()
        motion_profile = motion_service.extract_motion_features(upload_path, max_frames=30)
        
        inference_service = MechanismInferenceService()
        inference = inference_service.infer(device_name, motion_profile)
        
        # Build result
        result = {
            "device_name": device_name,
            "mechanism_summary": inference["mechanism_summary"],
            "motion_profile": {
                "dominant_motion": motion_profile.get("dominant_motion"),
                "cycle_estimate": motion_profile.get("cycle_estimate"),
                "confidence": motion_profile.get("confidence", 0.0),
                "sampled_frames": motion_profile.get("sampled_frames", 0),
            },
            "likely_faults": inference["likely_faults"],
            "repair_steps": inference["repair_steps"],
            "repurpose_options": inference["repurpose_options"],
            "safety_warnings": inference["safety_warnings"],
            "confidence": inference["confidence"],
        }
        
        processing_time = int((time.time() - start_time) * 1000)
        
        session_record.analysis_status = "completed"
        session_record.progress_percent = 100
        session_record.result_json = __import__("json").dumps(result)
        session_record.processing_time_ms = processing_time
        db.commit()
        
        health_monitor.active_sessions -= 1
        health_monitor.completed_sessions += 1
        
        logger.info(f"Background analysis completed: {session_id} in {processing_time}ms")
        
    except Exception as e:
        logger.error(f"Background analysis failed for {session_id}: {str(e)}")
        if db:
            session_record = db.query(VideoUploadSession).filter(
                VideoUploadSession.session_id == session_id
            ).first()
            if session_record:
                session_record.analysis_status = "failed"
                session_record.error_message = str(e)
                db.commit()
        health_monitor.record_error(str(e))
    finally:
        if db:
            db.close()
