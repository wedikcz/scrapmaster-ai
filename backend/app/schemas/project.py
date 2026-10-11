from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    """Base schema for projects."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: str = Field(default="draft", max_length=50)
    priority: str = Field(default="medium", max_length=50)
    target_completion_date: Optional[datetime] = None
    notes: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Schema for creating projects."""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating projects."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    target_completion_date: Optional[datetime] = None
    notes: Optional[str] = None


class ProjectRead(ProjectBase):
    """Schema for reading projects."""
    id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
