from datetime import datetime
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin, UserMixin


class Schematic(Base, TimestampMixin, UserMixin):
    """Schematic model for storing generated diagrams and technical guides."""

    __tablename__ = "schematics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    analysis_run_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    schematic_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )  # mechanical, electrical, repair_guide, assembly_guide
    content: Mapped[str] = mapped_column(Text, nullable=False)  # SVG, markdown, or HTML
    format: Mapped[str] = mapped_column(String(50), nullable=False)  # svg, markdown, html, pdf
    is_generated: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Schematic(id={self.id}, title={self.title}, type={self.schematic_type})>"
