from typing import Optional
from pydantic import BaseModel, Field

class MotionAnalysisMetric(BaseModel):
    """Real-time motion metric."""
    frame_index: int = Field(..., description="Frame index in sequence")
    motion_delta: float = Field(..., description="Absolute difference from previous frame")
    motion_type: str = Field(..., description="reciprocating, rotary, oscillatory, intermittent")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    velocity_estimate: Optional[float] = None
    acceleration_estimate: Optional[float] = None
    is_anomaly: bool = False
    anomaly_score: float = Field(default=0.0, ge=0.0, le=1.0)

class RealtimeAnalysisUpdate(BaseModel):
    """Real-time analysis progress update."""
    session_id: str
    frames_processed: int
    total_frames: int
    progress_percent: int
    current_motion_metrics: Optional[MotionAnalysisMetric] = None
    interim_motion_profile: Optional[dict] = None
    processing_speed_fps: Optional[float] = None
    eta_seconds: Optional[int] = None
    alerts: list[str] = Field(default_factory=list)

class FrameAnalysisRequest(BaseModel):
    """Request for frame-by-frame analysis."""
    session_id: str
    frame_data: str  # Base64 encoded image
    frame_index: int
    previous_frame_data: Optional[str] = None

class SystemHealthResponse(BaseModel):
    """System health and performance metrics."""
    status: str  # healthy, degraded, critical
    timestamp: str
    cpu_usage_percent: Optional[float] = None
    memory_usage_percent: Optional[float] = None
    disk_usage_percent: Optional[float] = None
    active_sessions: int = 0
    queued_analyses: int = 0
    completed_analyses: int = 0
    average_processing_time_ms: Optional[float] = None
    uptime_seconds: int = 0
    alerts: list[str] = Field(default_factory=list)
    last_error: Optional[str] = None
