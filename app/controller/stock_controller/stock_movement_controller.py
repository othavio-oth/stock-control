from app.service.stock_service.stock_movement_service import StockMovementService
from . import *

def get_all_movements(db):
    return StockMovementService.get_all_movements_service(db)

def get_current_stock(db):
    return StockMovementService.get_current_stock_service(db)

# def get_total_in_system_by_product(db, product_id):
#     return StockMovementService.get_total_in_system_by_product_service(db, product_id)


# def get_total_sold_by_cost_center_in_period_grouped_by_product(db, cost_center_id, start_date, end_date):
#     return StockMovementService.get_total_sold_by_cost_center_in_period_grouped_by_product_service(db, cost_center_id, start_date, end_date)


# def get_current_product_quantity(db):
#     return StockMovementService.get_current_product_quantity_service(db)

# def get_cost_center_stock_controller(cost_center_id: int, db):
#     return StockMovementService.get_cost_center_stock_service(cost_center_id, db)

# def get_monthly_sales_losses_stats_controller(db: Session, year: int = None):
#     return StockMovementService.get_monthly_sales_losses_stats_service(db, year)


def register_stock_loss_controller(db, loss_data):
    return StockMovementService.register_stock_loss_service(db, loss_data)

def register_client_sale_controller(db, sale_data):
    return StockMovementService.register_client_sale_service(db, sale_data)
