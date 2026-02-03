"""Create news table.

Revision ID: 20260203_1814_create_news
Revises: 20260203_1813_create_users
Create Date: 2026-02-03 18:14:00

[Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-DB-T01]
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20260203_1814_create_news'
down_revision: Union[str, None] = '20260203_1813_create_users'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-DB-T01]
    op.create_table(
        'news',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, 
                  server_default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('excerpt', sa.String(500), nullable=True),
        sa.Column('author_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='draft'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, 
                  server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, 
                  server_default=sa.text('NOW()')),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("status IN ('draft', 'published')", name='ck_news_status'),
    )
    # Create indexes for performance as specified in the plan
    op.create_index('idx_news_published_at_desc', 'news', 
                    [sa.text('published_at DESC NULLS LAST')])
    op.create_index('idx_news_status', 'news', ['status'])
    op.create_index('idx_news_author_id', 'news', ['author_id'])


def downgrade() -> None:
    op.drop_index('idx_news_author_id', table_name='news')
    op.drop_index('idx_news_status', table_name='news')
    op.drop_index('idx_news_published_at_desc', table_name='news')
    op.drop_table('news')
