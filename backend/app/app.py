from fastapi import FastAPI

from app.database import init_db
from app.routers.health import router as health_router
from app.routers.projects import router as projects_router
from app.routers.scrap import router as scrap_router
from app.routers.videos import router as videos_router

app = FastAPI(title="ScrapMaster Unified", version="0.1.0")
app.include_router(health_router)
app.include_router(videos_router)
app.include_router(scrap_router)
app.include_router(projects_router)

@app.on_event("startup")
def startup() -> None:
    init_db()

@app.get("/")
def root() -> dict:
    return {"app": "ScrapMaster Unified", "status": "online"}
