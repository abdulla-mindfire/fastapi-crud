"""create post table

Revision ID: f5e35bf81e0a
Revises: 
Create Date: 2022-11-30 16:03:47.544396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5e35bf81e0a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                            sa.Column('title', sa.String(), nullable=False))

    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
