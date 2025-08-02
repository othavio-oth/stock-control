"""logic delete in products

Revision ID: d9ab393e8ab9
Revises: 700515565df9
Create Date: 2025-08-01 14:52:18.998011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9ab393e8ab9'
down_revision: Union[str, None] = '700515565df9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
