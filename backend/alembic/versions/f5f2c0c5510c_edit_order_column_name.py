"""edit order column name

Revision ID: f5f2c0c5510c
Revises: d29733786f05
Create Date: 2026-03-01 15:04:31.423756

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f5f2c0c5510c"
down_revision: Union[str, Sequence[str], None] = "d29733786f05"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "goals_tasks",
        "order",
        new_column_name="order_num",
        existing_type=sa.Integer(),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "goals_tasks",
        "order_num",
        new_column_name="order",
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
