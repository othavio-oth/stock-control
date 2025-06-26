from . import *

def list_roles(db: Session = Depends(Config.DATABASE_URL)):
    return RolesService.list_roles(db)

def create_role(role_data: RoleBase, db: Session = Depends(Config.DATABASE_URL)):
    try:
        return RolesService.create_role(db, role_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

def edit_role(role_id: int, role_data: RoleBase, db: Session = Depends(Config.DATABASE_URL)):
    try:
        return RolesService.edit_role(db, role_id, role_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

def assign_role(role_id: int, user_id: int, db: Session = Depends(Config.DATABASE_URL)):
    return RolesService.assign_role(db, role_id, user_id)

def get_role_user(user_id: int, db: Session = Depends(Config.DATABASE_URL)):
    return RolesService.get_role_roles(db, user_id)

def delete_role(role_id: int, db: Session = Depends(Config.DATABASE_URL)):
    return RolesService.delete_role(db, role_id)

def delete_role_from_user(role_id: int, user_id: int, db: Session = Depends(Config.DATABASE_URL)):
    return RolesService.delete_role_from_user(db, role_id, user_id)