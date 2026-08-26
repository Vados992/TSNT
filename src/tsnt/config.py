"""Runtime configuration loaded from TSNT_* environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TSNT_", env_file=".env", extra="ignore")

    env: str = "development"
    log_level: str = "INFO"
    database_url: str = "sqlite+pysqlite:///:memory:"
    redis_url: str = "redis://localhost:6379/0"
    require_provenance: bool = True
    max_monte_carlo_runs: int = Field(default=100_000, ge=1, le=10_000_000)
    api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
