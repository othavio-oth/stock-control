from . import *

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,
        nickname=user.nickname,
        is_active=True,  # Marca o novo usuário como ativo
        is_superuser=user.is_superuser
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: User, user_update: UserUpdate):
    if user_update.password:
        db_user.hashed_password = hash_password(user_update.password)
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def mark_user_as_inactive(db: Session, db_user: User):
    db_user.is_active = False  # Marca o usuário como inativo
    db.commit()
    db.refresh(db_user)

def list_all_users(db: Session):
    # Consulta apenas usuários ativos, com join entre User, UserRole e Role
    users = (
        db.query(User)
        .filter(User.is_active == True)
        .outerjoin(UserRole, User.id == UserRole.user_id)
        .outerjoin(Role, UserRole.role_id == Role.id)
        .all()
    )

    # Formatar o resultado para incluir as roles no retorno
    result = []
    for user in users:
        roles = [ur.role.name for ur in user.roles]  # Extrair os nomes das roles
        role_name = roles[0] if roles else "None"  # Garantir que seja string ou "None"
        result.append(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "roles": role_name,
                "date_joined": user.date_joined,
                "last_login": user.last_login,           
            }
        )

    return result
