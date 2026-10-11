from datetime import datetime
from sqlalchemy import String, Text, Integer, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin, UserMixin


class ScrapItem(Base, TimestampMixin, UserMixin):
    """Scrap item inventory model."""

    __tablename__ = "scrap_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(180), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(100), index=True, nullable=True)  # motor, gearbox, electronics, etc.
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str | None] = mapped_column(String(200), nullable=True)  # where it came from
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(
        String(50),
        default="available",
        nullable=False,
    )  # available, in_use, broken, repurposed, archived
    estimated_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    safety_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    hazard_flags: Mapped[str | None] = mapped_column(Text, nullable=True)  # high_voltage, sharp_edges, etc.
    location: Mapped[str | None] = mapped_column(String(120), nullable=True)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<ScrapItem(id={self.id}, name={self.name}, category={self.category})>"
