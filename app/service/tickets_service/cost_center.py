from app.repository.tickets.cost_center_repository import create_cost_center, update_cost_center, get_all_cost_centers, get_cost_center_by_id, delete_cost_center
from app.models.tickets import CostCenter

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