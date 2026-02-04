"""News API router.

[Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
"""
from fastapi import APIRouter, Query

from app.application.news import ListPublishedNewsUseCase
from app.core.database import DBSession
from app.infrastructure.news import SQLAlchemyNewsRepository
from app.presentation.news.schemas import NewsListItem, NewsListResponse

router = APIRouter(prefix="/api/v1/news", tags=["news"])


@router.get("", response_model=NewsListResponse)
def list_published_news(
    db: DBSession,
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=50, description="Items per page"),
) -> NewsListResponse:
    """List published news articles.
    
    [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
    
    Public endpoint - no authentication required.
    Returns paginated list of published news articles sorted by published_at DESC.
    """
    repository = SQLAlchemyNewsRepository(session=db)
    use_case = ListPublishedNewsUseCase(news_repository=repository)
    result = use_case.execute(page=page, page_size=page_size)

    return NewsListResponse(
        items=[
            NewsListItem(
                id=article.id,
                title=article.title,
                excerpt=article.excerpt,
                author_name=article.author_name,
                published_at=article.published_at,
            )
            for article in result.items
        ],
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    )
