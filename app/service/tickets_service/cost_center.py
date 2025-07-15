from app.repository.tickets.cost_center_repository import create_cost_center, update_cost_center, get_all_cost_centers, get_cost_center_by_id, delete_cost_center, get_tickets_by_cost_center
from app.models.tickets import CostCenter, TicketProduct
from app.repository.tickets.tickets_repository import Ticket

class CostCenterService:
    @staticmethod
    def list_cost_centers(db):
        return get_all_cost_centers(db)

    @staticmethod
    def create_cost_center_service(db, center_data):
        existing_center = db.query(CostCenter).filter(CostCenter.name == center_data.name).first()
        if existing_center:
            raise ValueError("Centro de custo com este nome já existe.")
        return create_cost_center(db, center_data)

    @staticmethod
    def edit_cost_center(db, center_id, center_data):
        if not get_cost_center_by_id(db, center_id):
            raise ValueError("Centro de custo não encontrado.")
        return update_cost_center(db, center_id, center_data)

    @staticmethod
    def remove_cost_center(db, center_id):
        if not get_cost_center_by_id(db, center_id):
            raise ValueError("Centro de custo não encontrado.")
        return delete_cost_center(db, center_id)
    
    @staticmethod
    def get_tickets_by_cost_center(db, center_id):
        return get_tickets_by_cost_center(db, center_id)
    
    @staticmethod
    def get_ticket_products_by_cost_center(db, cost_center_id):
        tickets = get_tickets_by_cost_center(db, cost_center_id)
        ticket_ids = [t.id for t in tickets]

        return db.query(TicketProduct).filter(TicketProduct.ticket_id.in_(ticket_ids)).all()
    
    def get_cost_center_by_id(db, center_id):
        center = get_cost_center_by_id(db, center_id)
        if not center:
            raise ValueError("Centro de custo não encontrado.")
        return center