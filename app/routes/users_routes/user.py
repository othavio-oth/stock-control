from . import *

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

@router.get("/", response_model=List[UserResponseList])
def list_all_users(db: Session = Depends(get_db)):
    return list_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def read_user_details(user_id: int, db: Session = Depends(get_db)):
    return read_user(user_id, db)

@router.put("/{user_id}", response_model=UserResponse)
def update_user_details(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(user_id, user, db)

@router.delete("/{user_id}")
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return delete_user(user_id, db)