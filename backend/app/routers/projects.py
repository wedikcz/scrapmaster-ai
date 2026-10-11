from fastapi import APIRouter

from app.schemas.analysis import AnalysisRequest, AnalysisResult
from app.services.analysis_service import analyze_video

router = APIRouter(prefix="/api/v1")


@router.post("/videos/analyze", response_model=AnalysisResult)
def analyze_video_endpoint(payload: AnalysisRequest) -> AnalysisResult:
    data = analyze_video(device_name=payload.device_name, notes=payload.notes, video_url=payload.video_url)
    return AnalysisResult(**data)
