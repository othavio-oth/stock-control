from sqlalchemy.orm import Session
from app.repository.products.cost_taxation_repository import create_cost_taxation, get_all_cost_taxations, get_cost_taxation_by_id, delete_cost_taxation, update_cost_taxation

class CostTaxationService:
    @staticmethod
    def list_cost_taxations(db):
        return get_all_cost_taxations(db)

    @staticmethod
    def create_cost_taxation(db, cost_data):
        return create_cost_taxation(db, cost_data)

    @staticmethod
    def edit_cost_taxation(db, cost_id, cost_data):
        if not get_cost_taxation_by_id(db, cost_id):
            raise ValueError("Custo não encontrado.")
        return update_cost_taxation(db, cost_id, cost_data)

    @staticmethod
    def remove_cost_taxation(db, cost_id):
        if not get_cost_taxation_by_id(db, cost_id):
            raise ValueError("Custo não encontrado.")
        return delete_cost_taxation(db, cost_id)