"""seed roles admin and employee

Revision ID: 3f2a1c7b4e1a
Revises: a6653efb210a
Create Date: 2025-09-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f2a1c7b4e1a'
down_revision: Union[str, None] = 'a6653efb210a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    # Define a lightweight table representation for bulk_insert
    roles_table = sa.table(
        'roles',
        sa.column('name', sa.String),
        sa.column('description', sa.String),
    )

    desired = [
        {"name": "admin", "description": "Administrador"},
        {"name": "employee", "description": "Funcionário"},
    ]

    # Read existing role names to avoid unique constraint violations
    existing_rows = conn.execute(
        sa.text("SELECT name FROM roles WHERE name IN (:r1, :r2)")
    , {"r1": "admin", "r2": "employee"}).fetchall()

    existing = {row[0] for row in existing_rows}
    to_insert = [r for r in desired if r["name"] not in existing]

    if to_insert:
        op.bulk_insert(roles_table, to_insert)


def downgrade() -> None:
    # Remove only the seeded roles to keep other data intact
    op.execute(sa.text("DELETE FROM roles WHERE name IN (:r1, :r2)")
               .bindparams(r1="admin", r2="employee"))

