from fastapi import Query
from app.repository.stock.client_stock_repository import update_client_stock_quantity
from app.schemas.stock_schemas.stock_movement_schema import ClientStockResponse, ClientStockUpdateRequest
from app.service.stock_service.stock_movement_service import StockMovementService
from . import *
router = APIRouter(redirect_slashes=False, tags=["Client Stock NEW"])

@router.get(
    "",
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


@router.put("/", response_model=ClientStockResponse, status_code=status.HTTP_200_OK)
def edit_client_stock(
    data: ClientStockUpdateRequest,
    db: Session = Depends(get_db),
):
    """
    Atualiza (ou cria, se `upsert=True`) o estoque de um produto para um cost center.
    """
    try:
        result = update_client_stock_quantity(
            db=db,
            cost_center_id=data.cost_center_id,
            product_id=data.product_id,
            quantity=data.quantity,
            upsert=data.upsert,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")