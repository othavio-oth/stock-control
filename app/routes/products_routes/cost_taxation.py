from . import *

router = APIRouter()

@router.get("/cost_taxations/", response_model=List[CostTaxationResponse], tags=["Cost Taxations"])
def get_cost_taxations(db: Session = Depends(get_db)):
    return list_cost_taxations(db)

@router.post("/cost_taxations/", response_model=CostTaxationResponse, tags=["Cost Taxations"])
def create_new_cost_taxation(cost_data: CostTaxationCreate, db: Session = Depends(get_db)):
    return create_cost_taxation(cost_data, db)

@router.put("/cost_taxations/{cost_id}", response_model=CostTaxationResponse, tags=["Cost Taxations"])
def update_cost_taxation(cost_id: int, cost_data: CostTaxationUpdate, db: Session = Depends(get_db)):
    try:
        return edit_cost_taxation(cost_id, cost_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/cost_taxations/{cost_id}", tags=["Cost Taxations"])
def remove_cost_taxation(cost_id: int, db: Session = Depends(get_db)):
    return delete_cost_taxation(cost_id, db)