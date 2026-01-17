import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "Compliance Platform"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    SECRET_KEY: str = Field(default="change-me-in-production")

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/compliance"
    DATABASE_URL_SYNC: str = "postgresql://postgres:postgres@localhost:5432/compliance"
    REDIS_URL: str = "redis://localhost:6379/0"

    JWT_SECRET_KEY: str = Field(default="your-jwt-secret-key-min-32-chars")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_URL: str = "redis://localhost:6379/2"

    SPACY_MODEL: str = "en_core_web_trf"
    PRESIDIUM_ANALYZER_DEFAULT_LANGUAGES: str = "en"

    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 50
    STORAGE_TYPE: str = "local"

    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@compliance.example.com"

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60

    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:5173"]
    )
    CORS_ALLOW_CREDENTIALS: bool = True

    BCRYPT_ROUNDS: int = 12
    PASSWORD_MIN_LENGTH: int = 8
    OTP_EXPIRE_MINUTES: int = 10

    ENCRYPTION_KEY: str = "your-encryption-key-32-chars"

    @property
    def async_database_url(self) -> str:
        return self.DATABASE_URL

    @property
    def sync_database_url(self) -> str:
        return self.DATABASE_URL_SYNC

    def get_upload_dir(self) -> Path:
        return Path(self.UPLOAD_DIR)

    def get_max_file_size(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
