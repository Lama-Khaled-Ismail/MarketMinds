"""create reviews table

Revision ID: fc9be30b99f0
Revises: d7118e03eb6f
Create Date: 2024-07-05 18:57:30.833751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc9be30b99f0'
down_revision: Union[str, None] = 'd7118e03eb6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('review',
                    sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                    sa.Column('analysis_id', sa.Integer, sa.ForeignKey('analysis.id'), nullable=False),
                    sa.Column('text', sa.String, nullable=False),
                    sa.Column('score', sa.Boolean, nullable=False)
                    )



def downgrade() -> None:
    op.drop_table('review')
