import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.realtime import RealtimeAnalysisUpdate, SystemHealthResponse
from app.services.system_health import health_monitor
from app.models.realtime import VideoUploadSession

router = APIRouter(prefix="/realtime", tags=["realtime"])

logger = logging.getLogger(__name__)

# Store active WebSocket connections
active_connections: dict[str, WebSocket] = {}

@router.websocket("/ws/analysis/{session_id}")
async def websocket_analysis_endpoint(websocket: WebSocket, session_id: str, db: Session = Depends(get_db)):
    """WebSocket endpoint for real-time analysis updates."""
    await websocket.accept()
    active_connections[session_id] = websocket
    
    try:
        # Verify session exists
        session = db.query(VideoUploadSession).filter(
            VideoUploadSession.session_id == session_id
        ).first()
        
        if not session:
            await websocket.send_json({
                "type": "error",
                "message": "Session not found",
            })
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        # Send connection acknowledgment
        await websocket.send_json({
            "type": "connected",
            "session_id": session_id,
            "timestamp": str(__import__("datetime").datetime.utcnow()),
        })
        
        # Keep connection alive and listen for client messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            
    except WebSocketDisconnect:
        del active_connections[session_id]
        logger.info(f"WebSocket client disconnected: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error for {session_id}: {str(e)}")
        if session_id in active_connections:
            del active_connections[session_id]

async def broadcast_analysis_update(session_id: str, update: dict):
    """Broadcast analysis update to all connected clients."""
    if session_id in active_connections:
        try:
            websocket = active_connections[session_id]
            await websocket.send_json({
                "type": "analysis_update",
                "data": update,
            })
        except Exception as e:
            logger.error(f"Failed to broadcast update: {str(e)}")

@router.get("/health", response_model=SystemHealthResponse)
def get_system_health(db: Session = Depends(get_db)):
    """Get current system health and performance metrics."""
    report = health_monitor.get_performance_report()
    
    return SystemHealthResponse(
        status=report["status"],
        timestamp=report["timestamp"],
        cpu_usage_percent=report["system_metrics"].get("cpu_usage_percent"),
        memory_usage_percent=report["system_metrics"].get("memory_usage_percent"),
        disk_usage_percent=report["system_metrics"].get("disk_usage_percent"),
        active_sessions=report["session_stats"]["active"],
        queued_analyses=0,
        completed_analyses=report["session_stats"]["completed"],
        average_processing_time_ms=None,
        uptime_seconds=report["uptime_seconds"],
        alerts=report["alerts"],
        last_error=report["last_error"],
    )

@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    """Get detailed system metrics."""
    return health_monitor.get_performance_report()

@router.post("/sessions/{session_id}/heartbeat")
def session_heartbeat(session_id: str, db: Session = Depends(get_db)):
    """Keep-alive heartbeat for active sessions."""
    session = db.query(VideoUploadSession).filter(
        VideoUploadSession.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    
    return {
        "status": "alive",
        "session_id": session_id,
        "current_progress": session.progress_percent,
    }
