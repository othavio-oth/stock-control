from app.repository.stock.stock_movement_repository import create_system_in_movement, get_all_product_quantities_in_system, get_all_stock_movements, get_total_in_system_by_product, get_total_sold_by_cost_center_in_period_grouped_by_product

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
