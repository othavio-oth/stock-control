"""adicionar usuario de teste

Revision ID: 69333cad8d42
Revises: c3b640c7060c
Create Date: 2025-08-14 16:42:41.535923

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import bcrypt
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '69333cad8d42'
down_revision: Union[str, None] = 'c3b640c7060c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def upgrade():
    # 1. Definindo os dados iniciais com TODOS os campos obrigatórios
    users_data = [
        {
            "username": "teste",
            "email": "admin@teste.com",
            "hashed_password": hash_password("admin"),
            "full_name": "Administrador do Sistema",
            "is_active": True,
            "is_superuser": True,  # Agora explicitamente definido
            "nickname": None,  # Campo opcional explicitado
            "last_login": None  # Campo opcional explicitado
        },
    ]

    # 2. Inserção em lote com todos os campos
    op.bulk_insert(
        sa.table('users',
            sa.column('username'),
            sa.column('email'),
            sa.column('hashed_password'),
            sa.column('full_name'),
            sa.column('nickname'),
            sa.column('is_active'),
            sa.column('is_superuser'),
            sa.column('last_login'),
            sa.column('date_joined')
        ),
        [
            {**user, "date_joined": datetime.now()}
            for user in users_data
        ]
    )

def downgrade():
    op.drop_table('users')