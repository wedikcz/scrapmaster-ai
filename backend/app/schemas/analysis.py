from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    device_name: str = "salvaged device"
    video_url: str | None = None
    notes: str = ""


class AnalysisResult(BaseModel):
    device_name: str
    mechanism_summary: str
    motion_profile: dict
    likely_faults: list[str]
    repair_steps: list[str]
    repurpose_options: list[str]
    confidence: float
