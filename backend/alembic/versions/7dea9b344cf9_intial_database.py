"""intial database

Revision ID: 7dea9b344cf9
Revises: fa3ed1f5e4e7
Create Date: 2024-07-01 14:40:20.812520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dea9b344cf9'
down_revision: Union[str, None] = 'fa3ed1f5e4e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
