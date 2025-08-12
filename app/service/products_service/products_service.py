from fastapi import HTTPException
from app.models.tickets import CostCenter
from app.repository.products.products_repository import  create_product, get_all_products, search_products_by_term, update_product, delete_product, get_product_by_id
from sqlalchemy.orm import Session
from app.models.product import Product
class ProductService:

    
    @staticmethod
    def get_product(product_id, db):
        product = get_product_by_id(product_id, db)
        if not product:
            raise HTTPException(404,"Produto não encontrado.")
        return product
    
    @staticmethod
    def remove_product(db, product_id):
        product = ProductService.get_product(product_id, db)
        return delete_product(db, product)

    @staticmethod
    def create_product(db, product_data):
        return create_product(db, product_data)

    @staticmethod
    def edit_product(db, product_id, product_data):
        
        return update_product(db, product_id, product_data)

    
    @staticmethod
    def search_products(term,page, db):
        return search_products_by_term(term,page, db)
    
    @staticmethod
    def get_all_products_service(page,db):
        return get_all_products(page,db)
    

    
    # @staticmethod
    # def get_product_sales( db, product_id: int, cost_center_id: int, period_days: int = 30):
    #     if period_days <= 0:
    #         raise HTTPException(status_code=400, detail="Period must be positive")
        
    #     product = db.query(Product).get(product_id)
    #     if not product:
    #         raise HTTPException(status_code=404, detail="Product not found")
            
    #     cost_center = db.query(CostCenter).get(cost_center_id)
    #     if not cost_center:
    #         raise HTTPException(status_code=404, detail="Cost center not found")

    #     return get_product_sales(db, product_id, cost_center_id, period_days)