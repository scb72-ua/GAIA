"""News repository interface (port).

[Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
"""
from typing import Optional, Protocol
from uuid import UUID

from app.domain.news.entity import News


class NewsRepository(Protocol):
    """Repository interface for News persistence.
    
    This is a port in the Hexagonal Architecture pattern.
    Implementations (adapters) live in the infrastructure layer.
    """

    def list_published(self, page: int, page_size: int) -> tuple[list[News], int]:
        """List published news articles with pagination.
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            
        Returns:
            Tuple of (list of News entities, total count)
        """
        ...

    # [Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-BE-T01]
    def get_published_by_id(self, news_id: UUID) -> Optional[News]:
        """Get a published news article by ID.
        
        Args:
            news_id: The UUID of the news article
            
        Returns:
            News entity if found and published, None otherwise
        """
        ...
