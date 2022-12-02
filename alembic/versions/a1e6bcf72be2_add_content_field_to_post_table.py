"""add content field to  post table

Revision ID: a1e6bcf72be2
Revises: f5e35bf81e0a
Create Date: 2022-11-30 16:11:52.709819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1e6bcf72be2'
down_revision = 'f5e35bf81e0a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
