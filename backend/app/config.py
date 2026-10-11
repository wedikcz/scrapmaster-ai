from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ScrapMaster AI"
    environment: str = "development"
    database_url: str = "sqlite:///./scrapmaster.db"
    api_prefix: str = "/api/v1"
    secret_key: str = "development-secret-key-change-me"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
