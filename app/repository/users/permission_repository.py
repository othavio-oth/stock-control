from . import *

class PermissionRepository:
    @staticmethod
    def get_all_permissions(db: Session):
        return db.query(Permission).order_by(Permission.id).all()

    @staticmethod
    def get_permission_by_id(db: Session, permission_id: int):
        return db.query(Permission).filter(Permission.id == permission_id).first()

    @staticmethod
    def get_permission_by_name(db: Session, name: str):
        return db.query(Permission).filter(Permission.name == name).first()

    @staticmethod
    def create_permission(db: Session, new_permission: PermissionCreate):
        permission = Permission(name=new_permission.name, description=new_permission.description)
        db.add(permission)
        db.commit()
        db.refresh(permission)
        return permission

    @staticmethod
    def assign_permission_to_role(db: Session, role_id: int, permission_id: int):
        role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
        db.add(role_permission)
        db.commit()
        db.refresh(role_permission)
        return role_permission

    @staticmethod
    def remove_permission_from_role(db: Session, role_id: int, permission_id: int):
        role_permission = db.query(RolePermission).filter(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id
        ).first()
        if not role_permission:
            raise ValueError("Permission not assigned to role")
        db.delete(role_permission)
        db.commit()

    @staticmethod
    def get_permissions_for_role(db: Session, role_id: int):
        return (
            db.query(Permission)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .filter(RolePermission.role_id == role_id)
            .all()
        )

    @staticmethod
    def get_roles_for_permission(db: Session, permission_id: int):
        return (
            db.query(Role)
            .join(RolePermission, Role.id == RolePermission.role_id)
            .filter(RolePermission.permission_id == permission_id)
            .all()
       )