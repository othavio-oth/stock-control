from app.models.tickets import Ticket
from app.schemas.tickets_schemas.inventory_visit_schema import InventoryVisitCreate, InventoryVisitUpdate
from . import *

def list_tickets(page,db):
    return TicketService.list_tickets(page,db)

def create_ticket(ticket_data, db):
    import logging
    logging.info(f"Ticket created by user {ticket_data}")
    return TicketService.create_ticket(db, ticket_data)

def edit_ticket(ticket_id, ticket_data, db):
    return TicketService.edit_ticket(db, ticket_id, ticket_data)

def delete_ticket(ticket_id, db):
    try: 
        TicketService.remove_ticket(db, ticket_id)
        return {"message": "Ticket removido com sucesso."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

def add_product_to_ticket_controller(product_data, db):
    return TicketService.add_product(db, product_data)

def get_products_for_ticket_controller(ticket_id, db):
    return TicketService.get_products_for_ticket(db, ticket_id)

def get_ticket_products_controller(db):
    return TicketService.service_get_ticket_products(db)

def remove_product_from_ticket_controller(ticket_product_id, db):
    return TicketService.remove_product(db, ticket_product_id)

def get_tickets_by_cost_center_controller(cost_center_id, db):
    return TicketService.get_tickets_by_cost_center(db, cost_center_id)

def close_ticket_controller(id: int, db: Session = Depends(get_db)):
    return TicketService.close_ticket_and_move_stock(id, db)

def search_tickets_by_term_controller(search_term,page, db):
    return TicketService.search_tickets_by_term(search_term,page, db)


def process_sales_controller(ticket: Ticket, db: Session):
    return TicketService.process_sales(ticket, db)

def register_inventory_visit_controller(ticket_id: int, visit_data: InventoryVisitCreate, db: Session, recorded_by: int | None):
    return TicketService.register_inventory_visit(db, ticket_id, visit_data, recorded_by)

def update_inventory_visit_controller(ticket_id: int, visit_id: int, visit_data: InventoryVisitUpdate, db: Session, user_id: int | None):
    return TicketService.update_inventory_visit(db, ticket_id, visit_id, visit_data, user_id)

def list_inventory_visits_controller(ticket_id: int, db: Session, user_id: int | None):
    return TicketService.list_inventory_visits(db, ticket_id, user_id)

def get_ticket_cycle_products_controller(ticket_id: int, db: Session):
    return TicketService.get_ticket_cycle_products(db, ticket_id)

def get_cost_center_product_visits_controller(cost_center_id: int, product_ids: list[int] | None, db: Session):
    return TicketService.get_cost_center_product_visits(
        db,
        cost_center_id=cost_center_id,
        product_ids=product_ids,
    )

def get_cost_center_latest_visits_controller(cost_center_id: int, limit: int, ticket_id: int | None, db: Session):
    return TicketService.get_cost_center_latest_visits(
        db,
        cost_center_id=cost_center_id,
        limit=limit,
        ticket_id=ticket_id,
    )

def get_previous_approved_ticket_controller(ticket_id: int, db: Session):
    return TicketService.get_previous_approved_ticket_service(db, ticket_id)

def get_ticket_visit_summary_controller(ticket_id: int, db: Session):
    return TicketService.get_ticket_visit_summary(db, ticket_id)

def get_cost_center_last_visit_next_qty_controller(cost_center_id: int, db: Session):
    return TicketService.get_cost_center_last_visit_next_qty(db, cost_center_id)
