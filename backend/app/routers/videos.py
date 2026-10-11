from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "ScrapMaster Unified"}
