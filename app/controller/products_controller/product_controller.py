from typing import Optional


from . import *

def list_products(page,db):
    return ProductService.list_products(page,db)

def get_product(product_id, db):
    return ProductService.get_product(product_id, db)

def create_product(product_data, db):
    return ProductService.create_product(db, product_data)

def edit_product(product_id, product_data, db):
   try:
       return ProductService.edit_product(db, product_id, product_data)
   except ValueError as e:
       raise HTTPException(status_code=400, detail=str(e))

def delete_product(product_id, db):
    try:
       return ProductService.remove_product(db, product_id)
    except ValueError as e:
       raise HTTPException(status_code=400, detail=str(e))
   
def search_products_by_term_controller(term,page, db):
    return ProductService.search_products(term,page,db)

def get_all_products_no_pagination_controller(db):
    return ProductService.get_all_products_no_pagination_service(db)

def get_product_entry_history_controller(product_id: int, page: int, db: Session):
    return ProductService.get_product_entry_history(product_id,page,db)

# def get_product_sales_controller(product_id: int, cost_center_id: int, period_days: int, db: Session):
#     return ProductService.get_product_sales(db, product_id, cost_center_id, period_days)