"""News domain entity.

[Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class News:
    """News article domain entity.
    
    Represents a news article in the system with its current state.
    """
    id: UUID
    title: str
    content: str
    excerpt: Optional[str]
    author_id: UUID
    author_name: str  # Denormalized for display purposes
    status: str  # 'draft' | 'published'
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]

    def is_published(self) -> bool:
        """Check if the article is published."""
        return self.status == "published"

    def is_draft(self) -> bool:
        """Check if the article is a draft."""
        return self.status == "draft"
