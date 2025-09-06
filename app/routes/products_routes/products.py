from typing import Union
from fastapi import Query

from app.controller.products_controller.product_controller import get_all_products_controller, get_product, get_product_entry_history_controller,  search_products_by_term_controller
from app.schemas.list_all_schemas.list_all_responses import AllEntriesProductsResponse, AllProductsResponse

from . import *

router = APIRouter()


@router.get("/products/", include_in_schema=False)
@router.get("/products", response_model=Union[List[ProductResponse], AllProductsResponse], tags=["Products"])
def get_products(page:int = Query(None, ge=1),db: Session = Depends(get_db)):
    return get_all_products_controller(page,db)

@router.post("/products", include_in_schema=False)
@router.post("/products/", response_model=ProductResponse, tags=["Products"])
def create_new_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(product_data, db)

@router.put("/products/{product_id}/", include_in_schema=False)
@router.put("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    try:
        return edit_product(product_id, product_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/products/{product_id}/", include_in_schema=False)
@router.delete("/products/{product_id}", tags=["Products"])
def remove_product(product_id: int, db: Session = Depends(get_db)):
    return delete_product(product_id, db)

@router.get("/products/search/", include_in_schema=False)
@router.get("/products/search", response_model=AllProductsResponse, tags=["Products"])
def search_products(
    term: str,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    products = search_products_by_term_controller( term,page,db)
    return products

@router.get("/products/{product_id}/", include_in_schema=False)
@router.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return get_product(product_id, db)

@router.get("/products/{product_id}/entry-history/", include_in_schema=False)
@router.get("/products/{product_id}/entry-history", response_model=AllEntriesProductsResponse, tags=["Products"])
def get_product_entry_history(product_id: int,page: int = Query(1, ge=1),db: Session = Depends(get_db)):
    return get_product_entry_history_controller(product_id,page,db)


# @router.get("/products/{product_id}/sales", response_model=ProductSalesAnalyticsResponse, tags=["Products"])
# def get_product_sales(
#     product_id: int,
#     cost_center_id: int,
#     period_days: int = Query(30, gt=0),
#     db: Session = Depends(get_db)
# ):
#     return get_product_sales_controller(product_id, cost_center_id, period_days, db)
