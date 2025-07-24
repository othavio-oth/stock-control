from . import *

def list_products(db):
    return ProductService.list_products(db)

def create_product(product_data, db):
    return ProductService.create_product(db, product_data)

def edit_product(product_id, product_data, db):
   try:
       return ProductService.edit_product(db, product_id, product_data)
   except ValueError as e:
       raise HTTPException(status_code=400, detail=str(e))

def delete_product(product_id, db):
    try:
       return ProductService.remove_product(db, product_id, product_data)
    except ValueError as e:
       raise HTTPException(status_code=400, detail=str(e))