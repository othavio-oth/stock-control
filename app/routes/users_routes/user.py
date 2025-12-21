from . import *
from app.middleware.permission import get_current_user
from app.models.user import User
from app.schemas.users_schemas.user_schema import CurrentUserResponse, CurrentUserRole

router = APIRouter(redirect_slashes=False)

@router.get("/me", response_model=CurrentUserResponse, tags=["Users"])
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    roles_payload = [
        CurrentUserRole(id=ur.role.id, name=ur.role.name)
        for ur in (current_user.roles or [])
        if ur.role
    ]
    preferred_name = current_user.full_name or current_user.nickname or current_user.username
    return CurrentUserResponse(
        id=current_user.id,
        name=preferred_name or current_user.username,
        email=current_user.email,
        roles=roles_payload or None,
    )

@router.post("", include_in_schema=False)
@router.post("/", response_model=UserResponse, tags=["Users"])
def create_new_user(user: UserCreate, db: Session = Depends(get_db), _ = Depends(is_admin)):
    return create_user(user, db)

@router.get("", include_in_schema=False)
@router.get("/", response_model=List[UserResponseList], tags=["Users"])
def list_all_users(db: Session = Depends(get_db)):
    return list_users(db)

@router.get("/{user_id}/", include_in_schema=False)
@router.get("/{user_id}", response_model=UserResponse, tags=["Users"])
def read_user_details(user_id: int, db: Session = Depends(get_db)):
    return read_user(user_id, db)

@router.put("/{user_id}/", include_in_schema=False)
@router.put("/{user_id}", response_model=UserResponse, tags=["Users"])
def update_user_details(user_id: int, user: UserUpdate, db: Session = Depends(get_db), _ = Depends(is_admin)):
    return update_user(user_id, user, db)

@router.delete("/{user_id}/", include_in_schema=False)
@router.delete("/{user_id}", tags=["Users"])
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return delete_user(user_id, db)
