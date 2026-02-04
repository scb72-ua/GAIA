"""SQLAlchemy implementation of NewsRepository.

[Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.news import News
from app.infrastructure.news.models import NewsModel, UserModel


class SQLAlchemyNewsRepository:
    """SQLAlchemy implementation of the NewsRepository port.
    
    [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def list_published(self, page: int, page_size: int) -> tuple[list[News], int]:
        """List published news articles with pagination.
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            
        Returns:
            Tuple of (list of News entities, total count)
        """
        # Build base query for published articles
        base_query = (
            select(NewsModel)
            .join(UserModel, NewsModel.author_id == UserModel.id)
            .where(NewsModel.status == "published")
        )

        # Get total count
        count_query = select(func.count()).select_from(
            base_query.subquery()
        )
        total = self._session.execute(count_query).scalar() or 0

        # Get paginated results, sorted by published_at DESC
        offset = (page - 1) * page_size
        items_query = (
            base_query
            .order_by(NewsModel.published_at.desc().nulls_last())
            .offset(offset)
            .limit(page_size)
        )

        results = self._session.execute(items_query).scalars().all()

        # Map to domain entities
        news_list = [
            self._to_domain(model)
            for model in results
        ]

        return news_list, total

    def _to_domain(self, model: NewsModel) -> News:
        """Convert SQLAlchemy model to domain entity."""
        return News(
            id=model.id,
            title=model.title,
            content=model.content,
            excerpt=model.excerpt,
            author_id=model.author_id,
            author_name=model.author.name,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
            published_at=model.published_at,
        )
