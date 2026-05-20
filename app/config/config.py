from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Password Security Platform"
    ENV: str = Field(default="development")
    DEBUG: bool = True

    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # CORS
    ALLOWED_ORIGINS: List[str] = Field(default_factory=list)

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None  # e.g., "logs/app.log"

    # Security
    SECRET_KEY: str = "change-me"
    HASH_ITERATIONS: int = 100_000

    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # HIBP
    HIBP_ENABLED: bool = True
    HIBP_TIMEOUT: float = 10.0

    # Email (SMTP)
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_USE_TLS: bool = True
    EMAIL_SENDER: Optional[str] = None

    # Reports / Data
    REPORTS_DIR: str = "data/reports"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
