from datetime import datetime
from sqlalchemy import String, Text, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Alert(Base):
    """Alert model for system notifications and warnings."""

    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    alert_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )  # safety_warning, analysis_complete, export_ready, etc.
    severity: Mapped[str] = mapped_column(
        String(50),
        default="info",
        nullable=False,
    )  # info, warning, critical
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    related_resource_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    related_resource_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_acknowledged: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Alert(id={self.id}, type={self.alert_type}, severity={self.severity})>"
