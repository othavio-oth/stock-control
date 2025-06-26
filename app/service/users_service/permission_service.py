from app.repository.users.permission_repository import PermissionRepository
from app.schemas.users_schemas.permissions_schema import PermissionCreate, PermissionUpdate
from sqlalchemy.orm import Session

class PermissionService:
    @staticmethod
    def list_permissions(db: Session):
        return PermissionRepository.get_all_permissions(db)

    @staticmethod
    def create_permission(db: Session, new_permission: PermissionCreate):
        existing_permission = PermissionRepository.get_permission_by_name(db, new_permission.name)
        if existing_permission:
            raise ValueError(f"Permission '{new_permission.name}' already exists.")
        return PermissionRepository.create_permission(db, new_permission)

    @staticmethod
    def edit_permission(db: Session, permission_id: int, new_permission: PermissionUpdate):
        permission = PermissionRepository.get_permission_by_id(db, permission_id)
        if not permission:
            raise ValueError("Permission not found.")
        permission.name = new_permission.name
        permission.description = new_permission.description
        db.commit()
        db.refresh(permission)
        return permission

    @staticmethod
    def delete_permission(db: Session, permission_id: int):
        permission = PermissionRepository.get_permission_by_id(db, permission_id)
        if not permission:
            raise ValueError("Permission not found.")
        db.delete(permission)
        db.commit()

    @staticmethod
    def assign_permission(db: Session, role_id: int, permission_id: int):
        return PermissionRepository.assign_permission_to_role(db, role_id, permission_id)

    @staticmethod
    def remove_permission_from_role(db: Session, role_id: int, permission_id: int):
        PermissionRepository.remove_permission_from_role(db, role_id, permission_id)

    @staticmethod
    def get_role_permissions(db: Session, role_id: int):
        return PermissionRepository.get_permissions_for_role(db, role_id)
    
    @staticmethod
    def get_roles_from_permissions(db: Session, permission_id: int):
        return PermissionRepository.get_roles_for_permission(db, permission_id)