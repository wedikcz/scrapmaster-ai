from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class VideoAnalysisRun(Base):
    __tablename__ = "video_analysis_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    device_name: Mapped[str] = mapped_column(String(255), default="unknown device")
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    mechanism_summary: Mapped[str] = mapped_column(Text, default="")
    motion_profile: Mapped[str] = mapped_column(String(255), default="unknown")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    project: Mapped["Project"] = relationship(back_populates="analyses")
