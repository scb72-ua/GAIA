"""News domain module."""
from app.domain.news.entity import News
from app.domain.news.repository import NewsRepository

__all__ = ["News", "NewsRepository"]
