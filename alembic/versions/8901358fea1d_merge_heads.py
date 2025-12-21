"""merge heads

Revision ID: 8901358fea1d
Revises: 3f2a1c7b4e1a, 3f2b1c9d7a10, 69333cad8d42
Create Date: 2025-09-02 19:12:23.379865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8901358fea1d'
down_revision: Union[str, None] = ('3f2a1c7b4e1a', '3f2b1c9d7a10', '69333cad8d42')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
