"""seed_initial_data

Revision ID: 700515565df9
Revises: 9b6d251d9ec5
Create Date: 2025-08-01 10:18:46.545841

"""
import datetime
from typing import Sequence, Union

from alembic import op
import bcrypt
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '700515565df9'
down_revision: Union[str, None] = '9b6d251d9ec5'
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
            "username": "admin",
            "email": "admin@empresa.com",
            "hashed_password": hash_password("admin"),
            "full_name": "Administrador do Sistema",
            "is_active": True,
            "is_superuser": True,  # Agora explicitamente definido
            "nickname": None,  # Campo opcional explicitado
            "last_login": None  # Campo opcional explicitado
        },
        {
            "username": "usuario_teste",
            "email": "teste@empresa.com",
            "hashed_password": hash_password("teste"),
            "full_name": "Usuário de Teste",
            "is_active": True,
            "is_superuser": False,  # Valor padrão explicitado
            "nickname": "Zé Teste",
            "last_login": None
        }
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