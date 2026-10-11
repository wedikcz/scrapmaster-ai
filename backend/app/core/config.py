import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration with environment variable support."""

    # Application metadata
    app_name: str = "ScrapMaster AI"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True

    # Database
    database_url: str = "sqlite:///./data/scrapmaster.db"
    db_pool_size: int = 5
    db_echo: bool = False

    # API
    api_prefix: str = "/api/v1"
    api_title: str = "ScrapMaster AI Backend"
    api_description: str = "Inverse video engineering and scrap hardware management platform"

    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    refresh_token_expire_days: int = 7
    password_hash_algorithm: str = "bcrypt"
    cors_origins: list[str] = ["*"]

    # Storage and uploads
    local_storage_dir: str = "./data"
    upload_dir: str = "./data/uploads"
    export_dir: str = "./data/exports"
    max_upload_size_mb: int = 500
    max_video_duration_seconds: int = 3600
    allowed_video_formats: list[str] = ["mp4", "avi", "mov", "webm", "mkv"]

    # Motion analysis
    motion_frame_limit: int = 60
    motion_confidence_threshold: float = 0.4
    motion_delta_threshold: float = 20.0

    # Local AI inference
    enable_opencv: bool = True
    enable_ollama: bool = False
    ollama_base_url: str = "http://localhost:11434"
    enable_whisper: bool = False
    whisper_model: str = "base"

    # Monitoring and logging
    log_level: str = "INFO"
    enable_audit_logs: bool = True
    enable_metrics: bool = True
    metrics_export_interval_seconds: int = 60

    # Cache
    cache_ttl_seconds: int = 300
    enable_cache: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    def __post_init__(self) -> None:
        """Create required directories."""
        os.makedirs(self.local_storage_dir, exist_ok=True)
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.export_dir, exist_ok=True)


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()
