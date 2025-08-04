from datetime import datetime
from fastapi import HTTPException
from pytest import Session
from app.models.tickets import CostCenter
from app.repository.stock.stock_movement_repository import create_system_in_movement, get_all_product_quantities_in_system, get_all_stock_movements, get_cost_center_stock, get_monthly_sales_losses_stats, get_total_in_system_by_product, get_total_sold_by_cost_center_in_period_grouped_by_product

class StockMovementService:
    
    @staticmethod
    def get_all_movements_service(db):
        return get_all_stock_movements(db)
    
    @staticmethod
    def create_system_in_movement_service(system_in_data, db):
        return create_system_in_movement(system_in_data, db)
    
    @staticmethod
    def get_total_in_system_by_product_service(db, product_id):
        return get_total_in_system_by_product(db, product_id)

    
    @staticmethod
    def get_total_sold_by_cost_center_in_period_grouped_by_product_service(db, cost_center_id, start_date, end_date):
        return get_total_sold_by_cost_center_in_period_grouped_by_product(db, cost_center_id, start_date, end_date)
    

    @staticmethod
    def get_current_product_quantity_service(db):
        return get_all_product_quantities_in_system(db)
    
    @staticmethod
    def get_cost_center_stock_service(cost_center_id: int, db: Session):
        cost_center = db.query(CostCenter).filter(CostCenter.id == cost_center_id).first()
        if not cost_center:
            raise HTTPException(status_code=404, detail="Cost center not found")

        return get_cost_center_stock( cost_center_id, db)
    

    @staticmethod
    def get_monthly_sales_losses_stats_service(db: Session, year: int = None):
        return get_monthly_sales_losses_stats(db, year)