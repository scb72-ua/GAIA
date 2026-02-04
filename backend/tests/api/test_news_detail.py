"""API tests for news detail endpoint.

[Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-BE-T01]
"""
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient


class TestNewsDetailAPI:
    """Test suite for GET /api/v1/news/{id} endpoint."""

    # [Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-BE-T01]

    def test_get_published_article_returns_200(
        self,
        client: TestClient,
        published_news: list,
    ) -> None:
        """Scenario: GET /api/v1/news/{id} returns article."""
        article = published_news[0]
        response = client.get(f"/api/v1/news/{article.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(article.id)
        assert data["title"] == article.title
        assert "content" in data
        assert data["author_name"] == "Test Author"

    def test_nonexistent_article_returns_404(
        self,
        client: TestClient,
    ) -> None:
        """Scenario: 404 for non-existent article."""
        fake_id = uuid4()
        response = client.get(f"/api/v1/news/{fake_id}")

        assert response.status_code == 404
        assert "Noticia no encontrada" in response.json()["detail"]

    def test_draft_article_returns_404(
        self,
        client: TestClient,
        draft_news: list,
    ) -> None:
        """Scenario: 404 for draft article (no leak)."""
        draft_article = draft_news[0]
        response = client.get(f"/api/v1/news/{draft_article.id}")

        assert response.status_code == 404
        # Ensure no draft content is leaked
        response_text = response.text
        assert draft_article.title not in response_text
        assert draft_article.content not in response_text

    def test_invalid_uuid_returns_422(
        self,
        client: TestClient,
    ) -> None:
        """Invalid UUID format should return validation error."""
        response = client.get("/api/v1/news/invalid-uuid")

        assert response.status_code == 422
