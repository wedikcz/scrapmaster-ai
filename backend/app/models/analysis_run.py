from datetime import datetime
from sqlalchemy import String, Text, Integer, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin, UserMixin


class AnalysisRun(Base, TimestampMixin, UserMixin):
    """Video analysis run model for storing inference results."""

    __tablename__ = "analysis_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    device_name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    input_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    motion_hint: Mapped[str | None] = mapped_column(String(100), nullable=True)
    video_duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    # Output fields
    mechanism_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    likely_faults: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON list
    repair_steps: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON list
    repurpose_options: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON list
    safety_warnings: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON list
    
    # Analysis metadata
    dominant_motion: Mapped[str | None] = mapped_column(String(100), nullable=True)
    motion_confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    cycle_estimate: Mapped[float | None] = mapped_column(Float, nullable=True)
    sampled_frames: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    analysis_method: Mapped[str] = mapped_column(
        String(100),
        default="opencv-motion-analysis",
        nullable=False,
    )
    
    # Overall confidence
    overall_confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    json_payload: Mapped[str] = mapped_column(Text, nullable=False)  # Full JSON response
    is_exported: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    export_timestamp: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<AnalysisRun(id={self.id}, device={self.device_name}, confidence={self.overall_confidence})>"
