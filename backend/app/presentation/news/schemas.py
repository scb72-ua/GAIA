"""News API schemas (DTOs).

[Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class NewsListItem(BaseModel):
    """Schema for a news item in the list response."""
    id: UUID
    title: str
    excerpt: str | None
    author_name: str
    published_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class NewsListResponse(BaseModel):
    """Schema for the paginated news list response.
    
    [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
    """
    items: list[NewsListItem]
    total: int
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=50)


# [Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-BE-T01]
class NewsDetailResponse(BaseModel):
    """Schema for a single news article detail response."""
    id: UUID
    title: str
    content: str
    author_name: str
    published_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
