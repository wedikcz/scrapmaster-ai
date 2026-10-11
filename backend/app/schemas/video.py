from typing import Literal

from pydantic import BaseModel, Field


class ScrapItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    category: str | None = None
    source: str | None = None
    quantity: int = 1
    status: str = "available"
    description: str | None = None
    safety_notes: str | None = None


class ScrapItemCreate(ScrapItemBase):
    pass


class ScrapItemRead(ScrapItemBase):
    id: int

    model_config = {"from_attributes": True}


class MotionProfile(BaseModel):
    dominant_motion: str = Field(default="unknown")
    cycle_estimate: float | None = None
    confidence: float = 0.0
    sampled_frames: int = 0


class MechanicalInsight(BaseModel):
    device_name: str
    mechanism_summary: str
    motion_profile: MotionProfile
    likely_faults: list[str] = Field(default_factory=list)
    repair_steps: list[str] = Field(default_factory=list)
    repurpose_options: list[str] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)


class VideoAnalysisRequest(BaseModel):
    device_name: str = "salvaged mechanism"
    notes: str | None = None
    motion_hint: str | None = "reciprocating"
    video_duration_seconds: float | None = None
    frame_count: int | None = None


class VideoAnalysisResponse(BaseModel):
    device_name: str
    mechanism_summary: str
    motion_profile: MotionProfile
    likely_faults: list[str]
    repair_steps: list[str]
    repurpose_options: list[str]
    safety_warnings: list[str]
    confidence: float
