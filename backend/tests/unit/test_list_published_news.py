"""Unit tests for ListPublishedNewsUseCase.

[Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
"""
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.application.news.list_published import ListPublishedNewsUseCase, ListPublishedNewsResult
from app.domain.news.entity import News


class MockNewsRepository:
    """Mock repository for testing."""

    def __init__(self, articles: list[News], total: int | None = None) -> None:
        self.articles = articles
        self._total = total if total is not None else len(articles)

    def list_published(self, page: int, page_size: int) -> tuple[list[News], int]:
        """Return mock articles."""
        return self.articles, self._total


def make_news(title: str = "Test News") -> News:
    """Factory for test News entities."""
    now = datetime.now(tz=timezone.utc)
    return News(
        id=uuid4(),
        title=title,
        content="Test content",
        excerpt="Test excerpt",
        author_id=uuid4(),
        author_name="Test Author",
        status="published",
        created_at=now,
        updated_at=now,
        published_at=now,
    )


class TestListPublishedNewsUseCase:
    """Test suite for ListPublishedNewsUseCase."""

    # [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]

    def test_list_published_news_returns_articles(self) -> None:
        """Scenario: List published news with pagination."""
        articles = [make_news(f"Article {i}") for i in range(5)]
        repository = MockNewsRepository(articles=articles, total=5)
        use_case = ListPublishedNewsUseCase(news_repository=repository)

        result = use_case.execute(page=1, page_size=10)

        assert isinstance(result, ListPublishedNewsResult)
        assert len(result.items) == 5
        assert result.total == 5
        assert result.page == 1
        assert result.page_size == 10

    def test_empty_list_when_no_published_news(self) -> None:
        """Scenario: Empty list when no published news."""
        repository = MockNewsRepository(articles=[], total=0)
        use_case = ListPublishedNewsUseCase(news_repository=repository)

        result = use_case.execute()

        assert len(result.items) == 0
        assert result.total == 0

    def test_page_size_capped_at_50(self) -> None:
        """Page size should be capped at 50."""
        repository = MockNewsRepository(articles=[])
        use_case = ListPublishedNewsUseCase(news_repository=repository)

        result = use_case.execute(page_size=100)

        assert result.page_size == 50

    def test_page_minimum_is_1(self) -> None:
        """Page should be at least 1."""
        repository = MockNewsRepository(articles=[])
        use_case = ListPublishedNewsUseCase(news_repository=repository)

        result = use_case.execute(page=0)

        assert result.page == 1

    def test_page_size_minimum_is_1(self) -> None:
        """Page size should be at least 1."""
        repository = MockNewsRepository(articles=[])
        use_case = ListPublishedNewsUseCase(news_repository=repository)

        result = use_case.execute(page_size=0)

        assert result.page_size == 1
