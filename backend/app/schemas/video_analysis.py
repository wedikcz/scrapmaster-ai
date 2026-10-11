from typing import Optional
from pydantic import BaseModel, Field


class MotionProfile(BaseModel):
    """Motion profile extracted from video analysis."""
    dominant_motion: str = Field(..., description="Type of motion: reciprocating, rotary, oscillatory, intermittent")
    cycle_estimate: Optional[float] = Field(None, description="Estimated cycle duration in seconds")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for motion classification")
    sampled_frames: int = Field(default=0, description="Number of frames analyzed")
    analysis_method: Optional[str] = Field(None, description="Method used for analysis")

    class Config:
        json_schema_extra = {
            "example": {
                "dominant_motion": "reciprocating",
                "cycle_estimate": 0.85,
                "confidence": 0.82,
                "sampled_frames": 30,
                "analysis_method": "opencv-motion-analysis",
            }
        }


class VideoAnalysisRequest(BaseModel):
    """Request model for video analysis endpoint."""
    device_name: str = Field(default="salvaged mechanism", description="Name/identifier of the device")
    notes: Optional[str] = Field(None, description="User notes about the device")
    motion_hint: Optional[str] = Field(None, description="Hint about expected motion type")
    video_duration_seconds: Optional[float] = Field(None, description="Duration of the video")
    frame_count: Optional[int] = Field(30, description="Number of frames to sample")

    class Config:
        json_schema_extra = {
            "example": {
                "device_name": "salvaged gearbox",
                "notes": "Observable oscillation with mild end-play",
                "motion_hint": "reciprocating",
                "video_duration_seconds": 12.4,
                "frame_count": 30,
            }
        }


class VideoAnalysisResponse(BaseModel):
    """Response model for video analysis endpoint."""
    device_name: str
    mechanism_summary: str = Field(..., description="High-level summary of mechanism operation")
    motion_profile: MotionProfile
    likely_faults: list[str] = Field(default_factory=list, description="Probable issues or failure modes")
    repair_steps: list[str] = Field(default_factory=list, description="Recommended repair procedures")
    repurpose_options: list[str] = Field(default_factory=list, description="Possible alternative uses")
    safety_warnings: list[str] = Field(default_factory=list, description="Critical safety considerations")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence in the analysis")

    class Config:
        json_schema_extra = {
            "example": {
                "device_name": "salvaged gearbox",
                "mechanism_summary": "The mechanism converts oscillating motion into a cyclic output via cam-and-follower arrangement.",
                "motion_profile": {
                    "dominant_motion": "reciprocating",
                    "cycle_estimate": 0.9,
                    "confidence": 0.82,
                    "sampled_frames": 30,
                },
                "likely_faults": ["worn cam follower", "misaligned linkage", "lubrication loss"],
                "repair_steps": [
                    "Inspect follower path for wear and debris",
                    "Lubricate pivots and joints",
                    "Verify shaft alignment before re-testing",
                ],
                "repurpose_options": ["manual actuator", "reciprocating feed drive"],
                "safety_warnings": [
                    "Disconnect stored energy before handling",
                    "Use eye protection around moving parts",
                ],
                "confidence": 0.82,
            }
        }


class VideoUploadResponse(BaseModel):
    """Response after video upload."""
    file_id: str
    filename: str
    file_size_bytes: int
    upload_timestamp: str
    status: str = "uploaded"
