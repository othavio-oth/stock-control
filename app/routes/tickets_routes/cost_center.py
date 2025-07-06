from . import *

router = APIRouter()

@router.get("/cost_centers/", response_model=List[CostCenterResponse])
def get_cost_centers(db: Session = Depends(get_db)):
    return list_cost_centers(db)

@router.post("/cost_centers/", response_model=CostCenterResponse)
def create_new_cost_center(center_data: CostCenterCreate, db: Session = Depends(get_db)):
    try:
        return create_cost_center(center_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/cost_centers/{center_id}", response_model=CostCenterResponse)
def update_cost_center(center_id: int, center_data: CostCenterUpdate, db: Session = Depends(get_db)):
    try:
        return edit_cost_center(center_id, center_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/cost_centers/{center_id}")
def remove_cost_center(center_id: int, db: Session = Depends(get_db)):
    return delete_cost_center(center_id, db)