"""Unit tests for GetPublishedNewsDetailUseCase.

[Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-BE-T01]
"""
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.application.news.get_detail import GetPublishedNewsDetailUseCase, NewsNotFoundError
from app.domain.news.entity import News


class MockNewsRepository:
    """Mock repository for testing."""

    def __init__(self, article: News | None = None) -> None:
        self._article = article

    def get_published_by_id(self, news_id):
        """Return mock article."""
        return self._article


def make_news(title: str = "Test News") -> News:
    """Factory for test News entities."""
    now = datetime.now(tz=timezone.utc)
    return News(
        id=uuid4(),
        title=title,
        content="Full content of the article",
        excerpt="Test excerpt",
        author_id=uuid4(),
        author_name="Test Author",
        status="published",
        created_at=now,
        updated_at=now,
        published_at=now,
    )


class TestGetPublishedNewsDetailUseCase:
    """Test suite for GetPublishedNewsDetailUseCase."""

    # [Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-BE-T01]

    def test_returns_article_when_published(self) -> None:
        """Scenario: Returns article when published."""
        article = make_news("Published Article")
        repository = MockNewsRepository(article=article)
        use_case = GetPublishedNewsDetailUseCase(news_repository=repository)

        result = use_case.execute(news_id=article.id)

        assert result == article
        assert result.title == "Published Article"

    def test_raises_not_found_when_repository_returns_none(self) -> None:
        """Scenario: Raises NotFound when article is draft or missing."""
        repository = MockNewsRepository(article=None)
        use_case = GetPublishedNewsDetailUseCase(news_repository=repository)

        with pytest.raises(NewsNotFoundError):
            use_case.execute(news_id=uuid4())

    def test_error_message_contains_news_id(self) -> None:
        """Error message should contain the requested news ID."""
        repository = MockNewsRepository(article=None)
        use_case = GetPublishedNewsDetailUseCase(news_repository=repository)
        news_id = uuid4()

        with pytest.raises(NewsNotFoundError) as exc_info:
            use_case.execute(news_id=news_id)
        
        assert str(news_id) in str(exc_info.value)
