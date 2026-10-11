from datetime import datetime
from sqlalchemy import String, Text, Integer, Float, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin, UserMixin

class MotionAnalysis(Base, TimestampMixin):
    """Real-time motion analysis metrics."""
    __tablename__ = "motion_analysis"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    frame_index: Mapped[int] = mapped_column(Integer, nullable=False)
    motion_delta: Mapped[float] = mapped_column(Float, nullable=False)
    motion_type: Mapped[str] = mapped_column(String(100), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    velocity_estimate: Mapped[float | None] = mapped_column(Float, nullable=True)
    acceleration_estimate: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_anomaly: Mapped[bool] = mapped_column(Boolean, default=False)
    anomaly_score: Mapped[float] = mapped_column(Float, default=0.0)

class VideoUploadSession(Base, TimestampMixin, UserMixin):
    """Video upload session tracking."""
    __tablename__ = "video_upload_sessions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    device_name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    input_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    motion_hint: Mapped[str | None] = mapped_column(String(100), nullable=True)
    video_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    video_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    video_duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    frame_count: Mapped[int] = mapped_column(Integer, default=0)
    upload_status: Mapped[str] = mapped_column(String(50), default="pending")
    analysis_status: Mapped[str] = mapped_column(String(50), default="not_started")
    progress_percent: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    result_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

class RealtimeMetric(Base):
    """Real-time system metrics."""
    __tablename__ = "realtime_metrics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    metric_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=True)
    tags: Mapped[str | None] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self) -> str:
        return f"<RealtimeMetric(name={self.metric_name}, value={self.metric_value}, unit={self.unit})>"
