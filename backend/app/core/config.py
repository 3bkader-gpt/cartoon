from __future__ import annotations

from functools import lru_cache
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = Field(default="Cartoon Downloader API")
    api_prefix: str = Field(default="/api")
    api_key: str | None = Field(default=None)

    database_url: str = Field(default="sqlite+aiosqlite:///./data/db.sqlite")
    # Alembic needs a sync driver URL
    database_url_sync: str = Field(default="sqlite:///./data/db.sqlite")

    log_level: str = Field(default="INFO")
    enable_docs: bool = Field(default=True)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


class HealthStatus(BaseModel):
    browser_pool_size: int | None = None
    active_contexts: int | None = None
    failed_contexts: int | None = None
    last_latency_ms: float | None = None
    queue_depth: int | None = None
