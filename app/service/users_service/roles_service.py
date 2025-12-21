from app.repository.users.roles_repository import RolesRepository
from app.repository.users.user_repository import get_user_by_id
from sqlalchemy.orm import Session
from app.schemas.users_schemas.roles_schema import RoleBase

class RolesService:
    @staticmethod
    def list_roles(db: Session):
        return RolesRepository.get_all_roles(db)

    @staticmethod
    def create_role(db: Session, new_role: RoleBase):
        existing_role = RolesRepository.get_roles_by_name(db, new_role.name)
        if existing_role:
            raise ValueError(f"role '{new_role.name}' already exists.")
        return RolesRepository.create_role(db, new_role)
    
    @staticmethod
    def edit_role(db: Session, role_id: int, new_role: RoleBase):
        existing_role = RolesRepository.get_roles_by_id(db, role_id)
        if existing_role is None:
            raise ValueError("Role does not exist")
        return RolesRepository.edit_role(db, role_id, new_role)

    @staticmethod
    def assign_role(db: Session, role_id: int, user_id: int):
        existing_role = RolesRepository.get_roles_by_id(db, role_id)
        existing_user = get_user_by_id(db, user_id)
        
        if existing_role is None or existing_user is None:
            raise ValueError("Role or User does not exist")

        # Verifica se exite alguma associação
        existing_assignment = RolesRepository.get_role_assignment(db, user_id)
        import logging
        logging.info(existing_assignment)
        if existing_assignment:
            # atualiza a associação existente
            return RolesRepository.update_role_to_user(db, role_id, user_id)
        
        # Cria a nova associação, pois não existe ainda
        return RolesRepository.assign_role_to_user(db, role_id, user_id)


    @staticmethod
    def get_role_roles(db: Session, user_id: int):
        return RolesRepository.get_roles_for_user(db, user_id)
    
    @staticmethod
    def delete_role(db: Session, role_id: int):
        existing_role = RolesRepository.get_roles_by_id(db, role_id)
        if existing_role is None:
            raise ValueError("Role does not exist")
        return RolesRepository.delete_role(db, role_id)
    
    @staticmethod
    def delete_role_from_user(db: Session, role_id: int, user_id: int):
        existing_role = RolesRepository.get_roles_by_id(db, role_id)
        existing_user = get_user_by_id(db, user_id)
        if existing_role is None or existing_user is None:
            raise ValueError("Role or User does not exist")
        return RolesRepository.delete_role_from_user(db, role_id, user_id)
