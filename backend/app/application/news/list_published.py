"""List published news use case.

[Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
"""
from dataclasses import dataclass
from typing import Protocol

from app.domain.news import News


class NewsRepositoryPort(Protocol):
    """Port for news repository dependency."""
    def list_published(self, page: int, page_size: int) -> tuple[list[News], int]:
        ...


@dataclass
class ListPublishedNewsResult:
    """Result of listing published news."""
    items: list[News]
    total: int
    page: int
    page_size: int


class ListPublishedNewsUseCase:
    """Use case for listing published news articles.
    
    [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
    """

    def __init__(self, news_repository: NewsRepositoryPort) -> None:
        self._repository = news_repository

    def execute(self, page: int = 1, page_size: int = 10) -> ListPublishedNewsResult:
        """List published news with pagination.
        
        Args:
            page: Page number (1-indexed), defaults to 1
            page_size: Items per page, defaults to 10, max 50
            
        Returns:
            ListPublishedNewsResult with items, total, page, and page_size
        """
        # Enforce constraints
        page = max(1, page)
        page_size = min(max(1, page_size), 50)

        items, total = self._repository.list_published(page=page, page_size=page_size)

        return ListPublishedNewsResult(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )
