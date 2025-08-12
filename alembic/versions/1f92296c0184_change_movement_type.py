"""change movement type

Revision ID: 1f92296c0184
Revises: f04254c4be65
Create Date: 2025-08-11 22:43:41.808989

"""
from typing import Sequence, Union
from sqlalchemy import text

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1f92296c0184'
down_revision: Union[str, None] = 'f04254c4be65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ENUM_NAME = "movement_type"

def upgrade():
    bind = op.get_bind()

    # 1) Cria o tipo ENUM se não existir (EXECUTE com string literal)
    bind.execute(sa.text("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1
            FROM pg_type t
            JOIN pg_namespace n ON n.oid = t.typnamespace
            WHERE t.typname = 'movement_type'
        ) THEN
            EXECUTE 'CREATE TYPE movement_type AS ENUM (''supplier_purchase'',''to_client'',''client_sale'',''client_loss'',''supplier_loss'')';
        END IF;
    END$$;
    """))

    # 2) Converte a coluna para o novo ENUM (faz cast via texto + lower)
    bind.execute(sa.text(f"""
        ALTER TABLE stock_movements
        ALTER COLUMN movement_type
        TYPE {ENUM_NAME}
        USING LOWER(movement_type::text)::{ENUM_NAME};
    """))

def downgrade():
    bind = op.get_bind()

    # Volta para TEXT
    bind.execute(sa.text("""
        ALTER TABLE stock_movements
        ALTER COLUMN movement_type TYPE TEXT USING movement_type::text;
    """))

    # (Opcional) Dropar o tipo
    bind.execute(sa.text(f"DROP TYPE IF EXISTS {ENUM_NAME};"))