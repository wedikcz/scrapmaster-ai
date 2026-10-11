from app.routers.health import router as health_router
from app.routers.projects import router as projects_router
from app.routers.scrap import router as scrap_router
from app.routers.videos import router as videos_router

__all__ = [
    "health_router",
    "projects_router",
    "scrap_router",
    "videos_router",
]
