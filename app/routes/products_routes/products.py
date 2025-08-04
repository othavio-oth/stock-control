from fastapi import Query

from app.controller.products_controller.product_controller import get_all_products_no_pagination_controller, get_product, search_products_by_term_controller
from app.schemas.list_all_schemas.list_all_responses import AllProductsResponse
from app.schemas.products_schemas.products_schemas import ProductsPageResponse
from . import *

router = APIRouter()

@router.get("/products/", response_model=AllProductsResponse, tags=["Products"])
def get_products(page: int = Query(1, ge=1), db: Session = Depends(get_db)):
    return list_products(page,db)

@router.get("/products/no-pagination", response_model=List[ProductResponse], tags=["Products"])
def get_products(db: Session = Depends(get_db)):
    return get_all_products_no_pagination_controller(db)

@router.post("/products/", response_model=ProductResponse, tags=["Products"])
def create_new_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(product_data, db)

@router.put("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    try:
        return edit_product(product_id, product_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/products/{product_id}", tags=["Products"])
def remove_product(product_id: int, db: Session = Depends(get_db)):
    return delete_product(product_id, db)

@router.get("/products/search", response_model=AllProductsResponse, tags=["Products"])
def search_products(
    term: str,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    products = search_products_by_term_controller( term,page,db)
    return products

@router.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return get_product(product_id, db)


