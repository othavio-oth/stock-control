from . import *

class RolesRepository:
    @staticmethod
    def get_all_roles(db: Session):
        return db.query(Role).all()

    @staticmethod
    def get_roles_by_name(db: Session, name: str):
        return db.query(Role).filter(Role.name == name).first()
    
    @staticmethod
    def get_roles_by_id(db: Session, id: int):
        return db.query(Role).filter(Role.id == id).first()

    @staticmethod
    def create_role(db: Session, new_role: RoleBase):
        role = Role(name=new_role.name, description=new_role.description)
        db.add(role)
        db.commit()
        db.refresh(role)
        return role
    
    @staticmethod
    def edit_role(db: Session, role_id: int, new_role: RoleBase):
        role = RolesRepository.get_roles_by_id(db, role_id)
        role.name = new_role.name
        role.description = new_role.description
        db.commit()
        db.refresh(role)
        return role

    @staticmethod
    def assign_role_to_user(db: Session, role_id: int, user_id: int):
        role_user = UserRole(role_id=role_id, user_id=user_id)
        db.add(role_user)
        db.commit()
        db.refresh(role_user)
        return role_user

    @staticmethod
    def get_role_assignment(db: Session, user_id: int):
        return db.query(UserRole).filter(
            UserRole.user_id == user_id
        ).first()

    # update role to user
    @staticmethod
    def update_role_to_user(db: Session, role_id: int, user_id: int):
        existing_role_user = db.query(UserRole).filter(
            UserRole.user_id == user_id
        ).first()
        if existing_role_user is None:
            raise ValueError("Role not assigned to user")
        
        existing_role_user.role_id = role_id
        db.commit()
        return existing_role_user

    @staticmethod
    def get_roles_for_user(db: Session, user_id: int):
        return (
            db.query(Role)
            .join(UserRole, Role.id == UserRole.role_id)
            .filter(UserRole.user_id == user_id)
            .all()
        )
        
    @staticmethod
    def delete_role(db: Session, role_id: int):
        role = RolesRepository.get_roles_by_id(db, role_id)
        db.delete(role)
        db.commit()
        return {"message": "Role deleted successfully"}

    @staticmethod
    def delete_role_from_user(db: Session, role_id: int, user_id: int):
        role_user = db.query(UserRole).filter(
            UserRole.role_id == role_id,
            UserRole.user_id == user_id
        ).first()
        if not role_user:
            raise ValueError("Role not assigned to user")
        db.delete(role_user)
        db.commit()
        return {"message": "Role deleted from user successfully"}
    
