from . import *
router = APIRouter()

@router.get("/stock-products/", response_model=List[StockProductResponse])
def get_stock_products(db: Session = Depends(get_db)):
    return list_stock_products(db)

@router.post("/stock-products/", response_model=StockProductResponse)
def create_new_stock_product(stock_product_data: StockProductCreate, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    try:
        import logging
        logging.info(f"StockProduct created by user {user['id']}")
        return create_stock_product(stock_product_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/stock-products/{stock_product_id}", response_model=StockProductResponse)
def update_stock_product(stock_product_id: int, stock_product_data: StockProductUpdate, db: Session = Depends(get_db)):
    return edit_stock_product(stock_product_id, stock_product_data, db)

@router.delete("/stock-products/{stock_product_id}")
def remove_stock_product(stock_product_id: int, db: Session = Depends(get_db)):
    return delete_stock_product(stock_product_id, db)

@router.get("/stock-products-history/", response_model=List[StockProductHistoryResponse])
def get_stock_products_history(db: Session = Depends(get_db)):
    return list_stock_products_history(db)

@router.post("/stock-products-history/", response_model=StockProductHistoryResponse)
def create_new_stock_product_history(stock_product_history_data: StockProductHistoryCreate, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    try:
        import logging
        logging.info(f"StockProductHistory created by user {user['id']}")
        return create_stock_product_history(stock_product_history_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/stock-products-history/{stock_product_history_id}", response_model=StockProductHistoryResponse)
def update_stock_product_history(stock_product_history_id: int, stock_product_history_data: StockProductHistoryUpdate, db: Session = Depends(get_db)):
    return edit_stock_product_history(stock_product_history_id, stock_product_history_data, db)

@router.delete("/stock-products-history/{stock_product_history_id}")
def remove_stock_product_history(stock_product_history_id: int, db: Session = Depends(get_db)):
    return delete_stock_product_history(stock_product_history_id, db)
