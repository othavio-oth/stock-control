from . import *

router = APIRouter(redirect_slashes=False)

@router.get("/permissions/", response_model=List[PermissionResponse], tags=["Permissions"])
def get_all_permissions(db: Session = Depends(get_db)):
    return list_permissions(db)

@router.post("/permissions/", response_model=PermissionResponse, tags=["Permissions"])
def create_new_permission(new_permission: PermissionCreate, db: Session = Depends(get_db)):
    return create_permission(new_permission, db)

@router.put("/permissions/{permission_id}", response_model=PermissionResponse, tags=["Permissions"])
def update_permission(permission_id: int, new_permission: PermissionUpdate, db: Session = Depends(get_db)):
    return edit_permission(permission_id, new_permission, db)

@router.delete("/permissions/{permission_id}", tags=["Permissions"])
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    return remove_permission(permission_id, db)

@router.post("/roles/{role_id}/permissions/", response_model=PermissionRoleResponse, tags=["Permissions"])
def assign_permission_to_role(role_id: int, request: PermissionRequest = Body(...), db: Session = Depends(get_db)):
    return assign_permission(role_id, request.permission_id, db)

@router.delete("/roles/{role_id}/permissions/{permission_id}", tags=["Permissions"])
def remove_permission_from_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    return unassign_permission(role_id, permission_id, db)

@router.get("/roles/{role_id}/permissions/", response_model=List[PermissionResponse], tags=["Permissions"])
def get_all_role_permissions(role_id: int, db: Session = Depends(get_db)):
    return get_role_permissions(role_id, db)

@router.get("/permissions/{permission_id}/roles/", response_model=List[RoleResponse], tags=["Permissions"])
def get_all_roles_from_permissions(permission_id: int, db: Session = Depends(get_db)):
    return get_roles_from_permissions(permission_id, db)