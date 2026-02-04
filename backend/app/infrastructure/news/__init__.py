"""News infrastructure module."""
from app.infrastructure.news.models import NewsModel, UserModel
from app.infrastructure.news.repository import SQLAlchemyNewsRepository

__all__ = ["NewsModel", "UserModel", "SQLAlchemyNewsRepository"]
