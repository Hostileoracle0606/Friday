"""Add mood profiles table

Revision ID: 003_add_mood
Revises: 002_add_oauth
Create Date: 2024-01-03 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003_add_mood'
down_revision = '002_add_oauth'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'mood_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('valence', sa.Float(), nullable=False),
        sa.Column('arousal', sa.Float(), nullable=False),
        sa.Column('source', sa.String()),
        sa.Column('confidence', sa.Float()),
        sa.Column('metadata', sa.JSON()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_mood_profiles_user_created', 'mood_profiles', ['user_id', 'created_at'])


def downgrade() -> None:
    op.drop_index('ix_mood_profiles_user_created', 'mood_profiles')
    op.drop_table('mood_profiles')

