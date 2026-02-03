"""GAIA FastAPI Application Entry Point.

[Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-DB-T01]
"""
from fastapi import FastAPI

from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
