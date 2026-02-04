"""Pytest configuration and fixtures.

[Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
"""
import os
from collections.abc import Generator
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import get_db
from app.infrastructure.news.models import Base, NewsModel, UserModel
from app.main import app

# Test database URL
TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5455/gaia"
)

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Create a clean database session for testing."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with overridden database dependency."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session) -> UserModel:
    """Create a test user."""
    user = UserModel(
        id=uuid4(),
        email=f"test_{uuid4().hex[:8]}@example.com",
        name="Test Author",
        role="VECINO",
        created_at=datetime.now(tz=timezone.utc),
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def published_news(db_session: Session, test_user: UserModel) -> list[NewsModel]:
    """Create published news articles."""
    now = datetime.now(tz=timezone.utc)
    articles = []
    for i in range(5):
        article = NewsModel(
            id=uuid4(),
            title=f"Published Article {i + 1}",
            content=f"Content of article {i + 1}",
            excerpt=f"Excerpt {i + 1}",
            author_id=test_user.id,
            status="published",
            created_at=now,
            updated_at=now,
            published_at=now,
        )
        articles.append(article)
        db_session.add(article)
    db_session.commit()
    return articles


@pytest.fixture
def draft_news(db_session: Session, test_user: UserModel) -> list[NewsModel]:
    """Create draft news articles."""
    now = datetime.now(tz=timezone.utc)
    articles = []
    for i in range(3):
        article = NewsModel(
            id=uuid4(),
            title=f"Draft Article {i + 1}",
            content=f"Draft content {i + 1}",
            excerpt=f"Draft excerpt {i + 1}",
            author_id=test_user.id,
            status="draft",
            created_at=now,
            updated_at=now,
            published_at=None,
        )
        articles.append(article)
        db_session.add(article)
    db_session.commit()
    return articles
