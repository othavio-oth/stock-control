from . import *

router = APIRouter(redirect_slashes=False)

@router.get("/roles/", response_model=List[RoleResponse], tags=["Roles"])
def get_all_roles(db: Session = Depends(get_db)):
    return list_roles(db)

@router.post("/roles/", response_model=RoleResponse, tags=["Roles"])
def create_new_role(new_role: RoleBase, db: Session = Depends(get_db)):
    return create_role(new_role, db)

@router.put("/roles/{role_id}", response_model=RoleResponse, tags=["Roles"])
def update_role(role_id: int, role: RoleBase, db: Session = Depends(get_db)):
    return edit_role(role_id, role, db)

@router.post("/role/{role_id}/user/", response_model=RoleUserResponse, tags=["Roles"])
def assign_role_to_user(role_id: int, new_role_to_user: RoleRequest, db: Session = Depends(get_db)):
    return assign_role(role_id, new_role_to_user.user_id, db)

@router.get("/role/{user_id}/user/", response_model=List[RoleResponse], tags=["Roles"])
def get_all_role_user(user_id: int, db: Session = Depends(get_db)):
    return get_role_user(user_id, db)

@router.delete("/role/{role_id}/user/{user_id}", tags=["Roles"])
def delete_to_role(role_id: int, db: Session = Depends(get_db)):
    return delete_role(role_id, db)

@router.delete("/role/{role_id}/from_user/{user_id}", tags=["Roles"])
def delete_from_role(role_id: int, user_id: int, db: Session = Depends(get_db)):
    return delete_role_from_user(role_id, user_id, db)