from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ScrapItemBase(BaseModel):
    """Base schema for scrap items."""
    name: str = Field(..., min_length=1, max_length=180)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    source: Optional[str] = Field(None, max_length=200)
    quantity: int = Field(default=1, ge=1)
    status: str = Field(default="available", max_length=50)
    estimated_value: Optional[float] = Field(None, ge=0.0)
    safety_notes: Optional[str] = None
    hazard_flags: Optional[str] = None
    location: Optional[str] = Field(None, max_length=120)


class ScrapItemCreate(ScrapItemBase):
    """Schema for creating scrap items."""
    pass


class ScrapItemUpdate(BaseModel):
    """Schema for updating scrap items."""
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    status: Optional[str] = None
    estimated_value: Optional[float] = None
    safety_notes: Optional[str] = None
    hazard_flags: Optional[str] = None
    location: Optional[str] = None


class ScrapItemRead(ScrapItemBase):
    """Schema for reading scrap items."""
    id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
