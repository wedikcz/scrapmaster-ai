from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "scrapmaster-ai-backend",
        "environment": "development",
        "version": "0.1.0",
    }
