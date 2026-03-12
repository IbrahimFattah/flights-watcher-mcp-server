"""Configuration helpers for the MCP server."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "flight_deal_watcher.db"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    db_path: Path = Field(default=DEFAULT_DB_PATH)
    provider: str = Field(default="mock")
    log_level: str = Field(default="INFO", validation_alias=AliasChoices("LOG_LEVEL", "FLIGHT_DEAL_LOG_LEVEL"))

    model_config = SettingsConfigDict(
        env_prefix="FLIGHT_DEAL_",
        env_file=PROJECT_ROOT / ".env",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def resolved_db_path(self) -> Path:
        """Return an absolute path for the SQLite database file."""
        if self.db_path.is_absolute():
            return self.db_path
        return PROJECT_ROOT / self.db_path


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load settings once per process."""
    return Settings()
