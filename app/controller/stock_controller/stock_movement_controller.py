from app.service.stock_service.stock_entry_service import StockEntryService
from app.service.stock_service.stock_movement_service import StockMovementService
from . import *

def get_all_movements(db, movement_type: str | None = None, product_id: int | None = None):
    return StockMovementService.get_all_movements_service(db, movement_type=movement_type, product_id=product_id)

def get_current_stock(db):
    return StockMovementService.get_current_stock_service(db)

def reset_inventory_stock_controller(db):
    return StockMovementService.reset_inventory_stock_service(db)

def get_product_entries_controller(db, product_id: int, page: int, page_size: int):
    return StockEntryService.get_product_entries_service(db, product_id, page, page_size)

def delete_stock_entry_controller(db: Session, movement_id: int):
    return StockEntryService.delete_supplier_purchase_entry_service(db, movement_id)

def update_stock_entry_controller(db: Session, movement_id: int, dto):
    return StockEntryService.update_supplier_purchase_entry_service(db, movement_id, dto)

def add_stock_bulk_controller(db: Session, bulk_dto):
    return StockEntryService.add_stock_bulk_with_cost_average(db, bulk_dto)

def get_client_sales_history_controller(
    db: Session,
    cost_center_id: int,
    product_id: int | None,
    start_date,
    end_date,
):
    return StockMovementService.get_client_sales_history_service(
        db=db,
        cost_center_id=cost_center_id,
        product_id=product_id,
        start_date=start_date,
        end_date=end_date,
    )

def get_client_loss_history_controller(
    db: Session,
    cost_center_id: int,
    product_id: int | None,
    start_date,
    end_date,
):
    return StockMovementService.get_client_loss_history_service(
        db=db,
        cost_center_id=cost_center_id,
        product_id=product_id,
        start_date=start_date,
        end_date=end_date,
    )


def get_client_sales_and_loss_history_controller(
    db: Session,
    cost_center_id: int,
    product_id: int | None,
    start_date,
    end_date,
):
    return StockMovementService.get_client_sales_and_loss_history_service(
        db=db,
        cost_center_id=cost_center_id,
        product_id=product_id,
        start_date=start_date,
        end_date=end_date,
    )


def get_daily_sales_and_loss_grouped_by_cost_center_controller(
    db: Session,
    *,
    start_date,
    end_date,
    cost_center_ids: list[int] | None,
    product_id: int | None,
):
    return StockMovementService.get_daily_sales_and_loss_by_cost_center_service(
        db=db,
        start_date=start_date,
        end_date=end_date,
        cost_center_ids=cost_center_ids,
        product_id=product_id,
    )

def get_cycle_analysis_controller(
    db: Session,
    *,
    ticket_id: int,
    max_cycles: int,
):
    return StockMovementService.get_cycle_analysis_service(
        db=db,
        ticket_id=ticket_id,
        max_cycles=max_cycles,
    )


def get_sales_quantity_controller(
    db: Session,
    *,
    product_id: int,
    start_date,
    end_date,
    cost_center_id: int | None = None,
    retail_chain_id: int | None = None,
):
    total = StockMovementService.get_sales_quantity_service(
        db=db,
        product_id=product_id,
        start_date=start_date,
        end_date=end_date,
        cost_center_id=cost_center_id,
        retail_chain_id=retail_chain_id,
    )
    return total


def update_client_sale_for_day_controller(
    db: Session,
    *,
    cost_center_id: int,
    product_id: int,
    d,
    new_total_sold: int,
):
    total = StockMovementService.update_client_sale_for_day_service(
        db=db,
        cost_center_id=cost_center_id,
        product_id=product_id,
        d=d,
        new_total_sold=new_total_sold,
    )
    return total
