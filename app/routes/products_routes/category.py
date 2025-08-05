from app.controller.products_controller.category_controller import create_category, delete_category, edit_category, list_categories
from . import *

router = APIRouter()

@router.get("/categories/", response_model=List[CategoryResponse], tags=["Categories"])
def get_categories(db: Session = Depends(get_db)):
    return list_categories(db)

@router.post("/categories/", response_model=CategoryResponse, tags=["Categories"])
def create_new_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return create_category(category_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/categories/{category_id}", response_model=CategoryResponse,tags=["Categories"] )
def update_category(category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db)):
    try:
        return edit_category(category_id, category_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/categories/{category_id}", tags=["Categories"])
def remove_category(category_id: int, db: Session = Depends(get_db)):
    return delete_category(category_id, db)