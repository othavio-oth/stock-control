from datetime import datetime
from typing import Any
from app.controller.stock_controller.stock_movement_controller import create_system_in_movement, get_all_movements, get_cost_center_stock_controller, get_current_product_quantity, get_monthly_sales_losses_stats_controller, get_total_in_system_by_product, get_total_sold_by_cost_center_in_period_grouped_by_product
from app.schemas.stock_schemas.stock_movement_schema import StockMovementRead, SystemInStockMovement, TotalProductStockResponse
from . import *
router = APIRouter()

@router.get("/stock-movements", response_model=List[StockMovementRead], tags=["Stock Movements"])
def get_stock_movements(db: Session = Depends(get_db)):
    return get_all_movements(db)

@router.post("/stock-movements/system-in", response_model=SystemInStockMovement, tags=["Stock Movements"])
def create_system_in(system_in_data: SystemInStockMovement, db: Session = Depends(get_db)):
    return create_system_in_movement(system_in_data, db)

@router.get("/stock-movements/total", response_model=List[TotalProductStockResponse], tags=["Stock Movements"])
def get_total_in_system(db: Session = Depends(get_db)):
    return get_current_product_quantity(db)

@router.get("/stock-movements/monthly-sales-losses", 
           response_model=List[Dict[str, Any]], 
           tags=["Stock Movements"])
def get_monthly_stats(
    db: Session = Depends(get_db),
    year: int = None
):
    """
    Endpoint para estatísticas mensais de vendas e perdas
    """
    return get_monthly_sales_losses_stats_controller(db, year)
    

@router.get("/stock-movements/{product_id}", response_model=TotalProductStockResponse, tags=["Stock Movements"])
def get_stock_products(product_id: int,db: Session = Depends(get_db), ):
    return get_total_in_system_by_product(db, product_id)


@router.get("/stock-movements/cost-center/{cost_center_id}/period", response_model=List[TotalProductStockResponse], tags=["Stock Movements"])
def get_total_sold_by_cost_center_in_period(
    cost_center_id: int,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
):
    return get_total_sold_by_cost_center_in_period_grouped_by_product(
        db, cost_center_id, start_date, end_date
    )
    
@router.get("/stock-movements/cost-center/{cost_center_id}", response_model=List[TotalProductStockResponse], tags=["Stock Movements"])
def get_cost_center_stock(
    cost_center_id: int,
    db: Session = Depends(get_db),
):
    return get_cost_center_stock_controller(cost_center_id, db)

