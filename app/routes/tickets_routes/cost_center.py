from typing import Union
from fastapi import Query
from app.controller.tickets_controller.cost_center_controller import get_cost_center_by_id, get_ticket_products_by_cost_center, get_tickets_by_cost_center, search_cost_centers_by_term_controller
from app.repository.tickets.cost_center_repository import search_cost_centers_by_term
from app.schemas.list_all_schemas.list_all_responses import AllCostCentersResponse
from . import *

router = APIRouter(redirect_slashes=False)

@router.get("/cost_centers/", response_model=Union[AllCostCentersResponse, List[CostCenterResponse]], tags=["Cost Centers"])
def get_cost_centers(page:int = Query(None, ge=1),db: Session = Depends(get_db)):
    return list_cost_centers(page,db)

@router.post("/cost_centers/", response_model=CostCenterResponse, tags=["Cost Centers"] )
def create_new_cost_center(center_data: CostCenterCreate, db: Session = Depends(get_db)):
    try:
        return create_cost_center(center_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/cost_centers/{center_id}", response_model=CostCenterResponse, tags=["Cost Centers"])
def update_cost_center(center_id: int, center_data: CostCenterUpdate, db: Session = Depends(get_db)):
    try:
        return edit_cost_center(center_id, center_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/cost_centers/{center_id}", tags=["Cost Centers"])
def remove_cost_center(center_id: int, db: Session = Depends(get_db)):
    return delete_cost_center(center_id, db)


@router.get("/cost_centers/{center_id}/tickets/", response_model=List[TicketResponse], tags=["Cost Centers"])
def get_all_tickets_by_cost_center(center_id: int, db: Session = Depends(get_db)):
    try:
        return get_tickets_by_cost_center(center_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/cost_centers/{center_id}/tickets/products/",response_model=List[TicketProductResponse], tags=["Cost Centers"])
def get_ticket_products_by_cost_center_route(center_id: int, db: Session = Depends(get_db)):
    try:
        return get_ticket_products_by_cost_center(db, center_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.get("/cost_centers/{center_id}", response_model=CostCenterResponse, tags=["Cost Centers"])
def get_cost_center_by_center_id(center_id: int, db: Session = Depends(get_db)):
    try:
        return get_cost_center_by_id(center_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    

@router.get("/cost_centers/search", response_model=AllCostCentersResponse, tags=["Cost Centers"])
def search_cost_centers(
    term: str,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    
    cost_centers = search_cost_centers_by_term_controller( term,page,db)
    return cost_centers