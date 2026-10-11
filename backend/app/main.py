from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.core.database import init_db
from app.core.logging import setup_logging
from app.core.middleware import TimingMiddleware, ErrorHandlingMiddleware
from app.api.routes import health, videos, scrap, projects, realtime
from app.api.routes import videos_realtime
from app.services.system_health import health_monitor

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(TimingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(videos.router, prefix=settings.api_prefix)
app.include_router(videos_realtime.router, prefix=settings.api_prefix)
app.include_router(scrap.router, prefix=settings.api_prefix)
app.include_router(projects.router, prefix=settings.api_prefix)
app.include_router(realtime.router, prefix=settings.api_prefix)

@app.get("/")
async def root():
    report = health_monitor.get_performance_report()
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": report["status"],
        "uptime_seconds": report["uptime_seconds"],
    }

@app.get("/health")
async def health_endpoint():
    report = health_monitor.get_performance_report()
    return {
        "status": report["status"],
        "timestamp": report["timestamp"],
        "metrics": report["system_metrics"],
    }
