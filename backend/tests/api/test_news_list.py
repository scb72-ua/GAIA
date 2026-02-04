"""API tests for news list endpoint.

[Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
"""
import pytest
from fastapi.testclient import TestClient


class TestNewsListAPI:
    """Test suite for GET /api/v1/news endpoint."""

    # [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]

    def test_list_published_news_returns_articles(
        self,
        client: TestClient,
        published_news: list,
    ) -> None:
        """Scenario: GET /api/v1/news returns published articles."""
        response = client.get("/api/v1/news")

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) == 5
        assert data["total"] == 5

        # Each item should have required fields
        for item in data["items"]:
            assert "id" in item
            assert "title" in item
            assert "excerpt" in item
            assert "author_name" in item
            assert "published_at" in item

    def test_drafts_not_visible_to_public(
        self,
        client: TestClient,
        draft_news: list,
    ) -> None:
        """Scenario: Draft articles are not visible to public."""
        response = client.get("/api/v1/news")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 0
        assert data["total"] == 0

    def test_mixed_articles_only_published_returned(
        self,
        client: TestClient,
        published_news: list,
        draft_news: list,
    ) -> None:
        """Only published articles should be returned when mixed."""
        response = client.get("/api/v1/news")

        assert response.status_code == 200
        data = response.json()
        # Only 5 published, not 8 total (5 published + 3 draft)
        assert len(data["items"]) == 5
        assert data["total"] == 5

    def test_pagination_works(
        self,
        client: TestClient,
        published_news: list,
    ) -> None:
        """Scenario: Pagination works correctly."""
        response = client.get("/api/v1/news?page=1&page_size=2")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["page_size"] == 2

    def test_empty_state_returns_empty_array(
        self,
        client: TestClient,
    ) -> None:
        """Scenario: Empty state returns empty array."""
        response = client.get("/api/v1/news")

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_page_size_cannot_exceed_50(
        self,
        client: TestClient,
    ) -> None:
        """Page size should be rejected if over 50."""
        response = client.get("/api/v1/news?page_size=100")

        # FastAPI Query validation should reject this
        assert response.status_code == 422


class TestNewsListAPIIntegration:
    """Integration tests package."""
    pass
