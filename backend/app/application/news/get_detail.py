"""Get news detail use case.

[Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-BE-T01]
"""
from typing import Optional, Protocol
from uuid import UUID

from app.domain.news import News


class NewsRepositoryPort(Protocol):
    """Port for news repository dependency."""
    def get_published_by_id(self, news_id: UUID) -> Optional[News]:
        ...


class NewsNotFoundError(Exception):
    """Raised when a news article is not found or not accessible."""
    pass


class GetPublishedNewsDetailUseCase:
    """Use case for retrieving a single published news article.
    
    [Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-BE-T01]
    """

    def __init__(self, news_repository: NewsRepositoryPort) -> None:
        self._repository = news_repository

    def execute(self, news_id: UUID) -> News:
        """Get a published news article by ID.
        
        Args:
            news_id: UUID of the news article
            
        Returns:
            News entity
            
        Raises:
            NewsNotFoundError: If article not found or not published
        """
        article = self._repository.get_published_by_id(news_id)
        
        if article is None:
            raise NewsNotFoundError(f"News article {news_id} not found")
        
        return article
