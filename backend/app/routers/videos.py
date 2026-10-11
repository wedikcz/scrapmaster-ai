from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.scrap import ScrapItem
from app.schemas.video import VideoAnalysisRequest, VideoAnalysisResponse
from app.services.analysis_service import MotionAnalysisService

router = APIRouter(prefix="/api/v1")


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "scrapmaster-ai-backend"}


@router.get("/scrap/items")
def list_scrap_items(db: Session = Depends(get_db)):
    return db.query(ScrapItem).all()


@router.post("/scrap/items")
def create_scrap_item(payload: dict, db: Session = Depends(get_db)):
    item = ScrapItem(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.post("/videos/analyze", response_model=VideoAnalysisResponse)
def analyze_video(request: VideoAnalysisRequest):
    service = MotionAnalysisService()
    return service.analyze(request)
