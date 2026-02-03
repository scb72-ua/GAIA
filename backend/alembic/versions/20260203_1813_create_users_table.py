"""Create users table (stub for auth feature).

Revision ID: 20260203_1813_create_users
Revises: 
Create Date: 2026-02-03 18:13:00

[Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-DB-T01]
Note: This is a minimal stub - the full Auth feature will extend this table.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20260203_1813_create_users'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-DB-T01]
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, 
                  server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('role', sa.String(20), nullable=False, server_default='VECINO'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, 
                  server_default=sa.text('NOW()')),
        sa.CheckConstraint("role IN ('PUBLIC', 'VECINO', 'ADMIN')", name='ck_users_role'),
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=True)


def downgrade() -> None:
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')
