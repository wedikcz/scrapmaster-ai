from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, declared_attr
from app.core.database import Base


class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamps to models."""

    @declared_attr
    def created_at(self) -> Mapped[datetime]:
        return mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    @declared_attr
    def updated_at(self) -> Mapped[datetime]:
        return mapped_column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False,
        )


class UserMixin:
    """Mixin for user audit fields."""

    @declared_attr
    def created_by_user_id(self) -> Mapped[int | None]:
        return mapped_column(nullable=True)

    @declared_attr
    def updated_by_user_id(self) -> Mapped[int | None]:
        return mapped_column(nullable=True)
