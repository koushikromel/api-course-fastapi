"""add content column to post table

Revision ID: 74b9e67179e8
Revises: dafd9c6a9439
Create Date: 2024-02-09 17:17:22.618314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74b9e67179e8'
down_revision: Union[str, None] = 'dafd9c6a9439'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
