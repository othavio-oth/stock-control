"""track client stock timestamps

Revision ID: 9f3eee1b51f9
Revises: d1b67f1840a3
Create Date: 2025-11-20 12:12:26.424797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f3eee1b51f9'
down_revision: Union[str, None] = 'd1b67f1840a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column("client_stock", sa.Column("last_observed_at", sa.DateTime(timezone=True)))
    op.add_column("client_stock", sa.Column("last_zeroed_at", sa.DateTime(timezone=True)))
    op.add_column("client_sales_history", sa.Column("observed_at", sa.DateTime(timezone=True)))
    op.add_column("client_loss_history", sa.Column("observed_at", sa.DateTime(timezone=True)))


def downgrade() -> None:
    pass
