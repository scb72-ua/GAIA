"""News repository interface (port).

[Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
"""
from typing import Protocol

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
