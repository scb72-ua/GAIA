"""Application configuration and settings.

[Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-DB-T01]
"""
import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5455/gaia"

    # Application
    app_name: str = "GAIA API"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
