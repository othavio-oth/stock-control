from sqlalchemy.orm import Session
from app.repository.users.user_repository import (
    get_user_by_id, get_user_by_email, create_user, update_user, mark_user_as_inactive, list_all_users
)
from app.schemas.users_schemas.user_schema import UserCreate, UserUpdate, UserResponse

def create_new_user(db: Session, user: UserCreate):
    existing_user = get_user_by_email(db, user.email)
    if existing_user and existing_user.is_active:
        raise ValueError("Email já está em uso por um usuário ativo")
    return create_user(db, user)

def service_list_users(db: Session):
    return list_all_users(db)

def get_user_details(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise ValueError("Usuário não encontrado ou está inativo")
    return user

def modify_user(db: Session, user_id: int, user_update: UserUpdate):
    user = get_user_by_id(db, user_id)
    if not user:
        raise ValueError("Usuário não encontrado ou está inativo")
    return update_user(db, user, user_update)

def remove_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise ValueError("Usuário não encontrado ou já está inativo")
    mark_user_as_inactive(db, user)