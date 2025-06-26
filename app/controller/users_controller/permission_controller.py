from . import *

def list_permissions(db: Session):
    return PermissionService.list_permissions(db)

def create_permission(permission_data: PermissionBase, db: Session):
    try:
        return PermissionService.create_permission(db, permission_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

def edit_permission(permission_id: int, permission: str, db: Session):
    try:
        return PermissionService.edit_permission(db, permission_id, permission)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

def remove_permission(permission_id: int, db: Session):
    try:
        PermissionService.delete_permission(db, permission_id)
        return {"detail": "Permission deleted successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

def assign_permission(role_id: int, permission_id: int, db: Session):
    return PermissionService.assign_permission(db, role_id, permission_id)

def unassign_permission(role_id: int, permission_id: int, db: Session):
    try:
        PermissionService.remove_permission_from_role(db, role_id, permission_id)
        return {"detail": "Permission removed from role"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

def get_role_permissions(role_id: int, db: Session):
    return PermissionService.get_role_permissions(db, role_id)

def get_roles_from_permissions(permission_id: int, db: Session):
    return PermissionService.get_roles_from_permissions(db, permission_id)
