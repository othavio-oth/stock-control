"""bridge placeholder for legacy revision 69333cad8d42

Revision ID: 69333cad8d42
Revises: 50469bb88a12
Create Date: 2025-09-01 00:00:00.000000

Purpose:
- Some databases have alembic_version set to '69333cad8d42', which
  does not exist in the current repo. This no-op migration allows Alembic
  to locate that revision and upgrade to newer heads without altering the
  schema at this step.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa: F401


# revision identifiers, used by Alembic.
revision: str = '69333cad8d42'
down_revision: Union[str, None] = '50469bb88a12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # No-op: placeholder to bridge legacy DB state to current chain
    pass


def downgrade() -> None:
    # No-op: removing this placeholder would require manual version stamping
    pass

