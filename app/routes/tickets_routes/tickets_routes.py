from . import *
from app.middleware.auth_handler import get_current_user

router = APIRouter()

@router.get("/tickets/", response_model=List[TicketResponse])
def get_tickets(db: Session = Depends(get_db)):
    return list_tickets(db)

@router.post("/tickets/", response_model=TicketResponse)
def create_new_ticket(ticket_data: TicketCreate, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    try:
        import logging
        ticket_data.created_by = user['id']
        result = create_ticket(ticket_data, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, ticket_data: TicketResponse, db: Session = Depends(get_db)):
    return edit_ticket(ticket_id, ticket_data, db)

@router.delete("/tickets/{ticket_id}")
def remove_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return delete_ticket(ticket_id, db)

@router.get("/tickets/{ticket_id}/products/", response_model=List[int])
def get_products_for_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return get_products_for_ticket_controller(ticket_id, db)

@router.get("/tickets/products/", response_model=List[TicketProductResponse])
def get_ticket_products_route(db: Session = Depends(get_db)):
    return get_ticket_products_controller(db)

@router.post("/tickets/products/", response_model=TicketProductResponse)
def add_product_to_ticket_route(product_data: TicketProductCreate, db: Session = Depends(get_db)):
    return add_product_to_ticket_controller(product_data, db)

@router.delete("/tickets/products/{ticket_product_id}")
def remove_product_from_ticket_route(ticket_product_id: int, db: Session = Depends(get_db)):
    return remove_product_from_ticket_controller(ticket_product_id, db)