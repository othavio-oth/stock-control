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
    # 1) Dados dos usuários a semear
    users_data = [
        {
            "username": "admin",
            "email": "admin@empresa.com",
            "password_plain": "admin",
            "full_name": "Administrador do Sistema",
            "is_active": True,
            "is_superuser": True,
            "nickname": None,
            "last_login": None,
        },
        {
            "username": "usuario_teste",
            "email": "teste@empresa.com",
            "password_plain": "teste",
            "full_name": "Usuário de Teste",
            "is_active": True,
            "is_superuser": False,
            "nickname": "Zé Teste",
            "last_login": None,
        },
    ]

    conn = op.get_bind()
    stmt = sa.text(
        """
        INSERT INTO users (
            username, email, hashed_password, full_name, nickname,
            is_active, is_superuser, last_login, date_joined
        ) VALUES (
            :username, :email, :hashed_password, :full_name, :nickname,
            :is_active, :is_superuser, :last_login, :date_joined
        )
        ON CONFLICT DO NOTHING
        """
    )

    now = datetime.now()
    for u in users_data:
        params = {
            "username": u["username"],
            "email": u["email"],
            "hashed_password": hash_password(u["password_plain"]),
            "full_name": u["full_name"],
            "nickname": u["nickname"],
            "is_active": u["is_active"],
            "is_superuser": u["is_superuser"],
            "last_login": u["last_login"],
            "date_joined": now,
        }
        conn.execute(stmt, params)

def downgrade():
    # Remove apenas os usuários semeados por esta revisão
    op.execute(
        sa.text(
            "DELETE FROM users WHERE email IN (:e1, :e2)"
        ).bindparams(e1="admin@empresa.com", e2="teste@empresa.com")
    )
