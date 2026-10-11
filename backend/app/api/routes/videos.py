from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.video_analysis import VideoAnalysisResponse
from app.services.motion_analysis import MotionAnalysisService
from app.services.mechanism_inference import MechanismInferenceService

router = APIRouter(prefix="/videos", tags=["videos"])


@router.post("/analyze", response_model=VideoAnalysisResponse)
async def analyze_video(
    device_name: str = Form("salvaged mechanism"),
    notes: str | None = Form(None),
    motion_hint: str | None = Form(None),
    frame_count: int = Form(30),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Video file is required")

    upload_dir = "./data/uploads"
    import os
    os.makedirs(upload_dir, exist_ok=True)

    target_path = f"{upload_dir}/{file.filename}"
    contents = await file.read()
    with open(target_path, "wb") as f:
        f.write(contents)

    motion_service = MotionAnalysisService()
    motion_profile = motion_service.extract_motion_features(target_path, max_frames=frame_count)

    inference_service = MechanismInferenceService()
    inference = inference_service.infer(device_name, motion_profile, notes, motion_hint)

    return VideoAnalysisResponse(
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
