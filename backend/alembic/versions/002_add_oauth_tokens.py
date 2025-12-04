"""Add OAuth tokens table

Revision ID: 002_add_oauth
Revises: 001_initial
Create Date: 2024-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_add_oauth'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'oauth_tokens',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('provider', sa.String(), nullable=False),
        sa.Column('access_token', sa.Text(), nullable=False),
        sa.Column('refresh_token', sa.Text()),
        sa.Column('token_expires_at', sa.DateTime(timezone=True)),
        sa.Column('scope', sa.String()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('ix_oauth_tokens_user_provider', 'oauth_tokens', ['user_id', 'provider'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_oauth_tokens_user_provider', 'oauth_tokens')
    op.drop_table('oauth_tokens')


