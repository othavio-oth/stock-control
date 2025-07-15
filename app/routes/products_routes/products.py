from . import *

router = APIRouter()

@router.get("/products/", response_model=List[ProductResponse], tags=["Products"])
def get_products(db: Session = Depends(get_db)):
    return list_products(db)

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