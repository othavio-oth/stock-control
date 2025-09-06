from datetime import datetime
from typing import Any

from fastapi import Query
from app.controller.stock_controller.stock_movement_controller import  get_all_movements, get_current_stock, register_stock_loss_controller, register_client_sale_controller
from app.models.stockMovement import StockMovement
from app.schemas.stock_schemas.stock_movement_schema import ClientStockResponse, InventoryResponse, StockMovementLost, StockMovementRead, SupplierPurchaseDTO, TotalProductStockResponse, RegisterClientSalesDTO
from app.service.stock_service.stock_movement_service import StockMovementService
from . import *
router = APIRouter(redirect_slashes=False)




@router.get("/stock-movements/", include_in_schema=False)
@router.get("/stock-movements", response_model=List[StockMovementRead], tags=["Stock Movements"])
def get_stock_movements(db: Session = Depends(get_db)):
    return get_all_movements(db)



@router.get("/stock-movements/current-stock/", include_in_schema=False)
@router.get("/stock-movements/current-stock", response_model=List[InventoryResponse], tags=["Stock Movements"])
def get_total_in_system(db: Session = Depends(get_db)):
    return get_current_stock(db)



@router.post("/add-stock/", include_in_schema=False)
@router.post("/add-stock", response_model=StockMovementRead, status_code=status.HTTP_201_CREATED, tags=["Stock Movements"])
def add_stock( dto:SupplierPurchaseDTO, db: Session = Depends(get_db),):
    return StockMovementService.add_stock_with_cost_average(db, dto)

@router.get(
    "/client-stock/",
    include_in_schema=False,
)
@router.get(
    "/client-stock",
    response_model=List[ClientStockResponse],
    summary="Estoque do cliente por produto",
    description="Retorna o estoque atual do cliente (por produto). "
                "Parâmetros opcionais: product_ids CSV e include_zero.",
    tags=["Client Stock"],
)
def get_client_stock(
    cost_center_id: int = Query(..., description="ID do cost center"),
    product_ids: Optional[str] = Query(
        None, description="CSV de product_ids para filtrar (ex: 1,2,3)"
    ),
    include_zero: bool = Query(
        False, description="Se true, retorna 0 para ids solicitados e não encontrados"
    ),
    db: Session = Depends(get_db),
):
    ids_list: Optional[List[int]] = None
    if product_ids:
        try:
            ids_list = [int(x) for x in product_ids.split(",") if x.strip()]
        except ValueError:
            raise HTTPException(status_code=400, detail="product_ids inválido")

    data = StockMovementService.get_client_stock_service(
        db=db,
        cost_center_id=cost_center_id,
        product_ids=ids_list,
        include_zero=include_zero,
    )
    return data
# @router.get("/stock-movements/monthly-sales-losses", 
#            response_model=List[Dict[str, Any]], 
#            tags=["Stock Movements"])
# def get_monthly_stats(
#     db: Session = Depends(get_db),
#     year: int = None
# ):
#     """
#     Endpoint para estatísticas mensais de vendas e perdas
#     """
#     return get_monthly_sales_losses_stats_controller(db, year)
    

# @router.get("/stock-movements/{product_id}", response_model=TotalProductStockResponse, tags=["Stock Movements"])
# def get_stock_products(product_id: int,db: Session = Depends(get_db), ):
#     return get_total_in_system_by_product(db, product_id)


# @router.get("/stock-movements/cost-center/{cost_center_id}/period", response_model=List[TotalProductStockResponse], tags=["Stock Movements"])
# def get_total_sold_by_cost_center_in_period(
#     cost_center_id: int,
#     start_date: datetime,
#     end_date: datetime,
#     db: Session = Depends(get_db),
# ):
#     return get_total_sold_by_cost_center_in_period_grouped_by_product(
#         db, cost_center_id, start_date, end_date
#     )
    
# @router.get("/stock-movements/cost-center/{cost_center_id}", response_model=List[TotalProductStockResponse], tags=["Stock Movements"])
# def get_cost_center_stock(
#     cost_center_id: int,
#     db: Session = Depends(get_db),
# ):
#     return get_cost_center_stock_controller(cost_center_id, db)


@router.post("/stock-movements/losses/", include_in_schema=False)
@router.post("/stock-movements/losses",response_model=StockMovementRead,status_code=status.HTTP_201_CREATED, tags=["Stock Movements"])
def create_loss_record(
    loss_data: StockMovementLost,
    db: Session = Depends(get_db)):
    try:
        return register_stock_loss_controller(db, loss_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))

@router.post("/stock-movements/sales/", include_in_schema=False)
@router.post("/stock-movements/sales",response_model=StockMovementRead,status_code=status.HTTP_201_CREATED, tags=["Stock Movements"])
def create_sale_record(
    sale_data: RegisterClientSalesDTO,
    db: Session = Depends(get_db)):
    try:
        return register_client_sale_controller(db, sale_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))
