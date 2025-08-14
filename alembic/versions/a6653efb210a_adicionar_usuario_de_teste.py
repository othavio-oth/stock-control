"""adicionar usuario de teste

Revision ID: a6653efb210a
Revises: 50469bb88a12
Create Date: 2025-08-14 17:26:40.973989

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import bcrypt
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6653efb210a'
down_revision: Union[str, None] = '50469bb88a12'
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