"""create analysis table

Revision ID: d7118e03eb6f
Revises: 7dea9b344cf9
Create Date: 2024-07-05 15:49:59.625324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7118e03eb6f'
down_revision: Union[str, None] = '7dea9b344cf9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('analysis', 
                    sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                    sa.Column('brand_id', sa.Integer, sa.ForeignKey('brand.id'), nullable=False),
                    sa.Column('positive', sa.Integer, nullable=False),
                    sa.Column('negaitive', sa.Integer, nullable= False),
                    sa.Column('num_reviews', sa.Integer, nullable= False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),
                    sa.Column('platform', sa.String, nullable=False),
                    sa.Column('language', sa.String, nullable=False)
                    )
    


def downgrade() -> None:
    op.drop_table('analysis')
