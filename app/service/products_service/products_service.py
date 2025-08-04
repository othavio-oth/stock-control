from typing import Optional
from fastapi import HTTPException
from app.repository.products.products_repository import get_all_active_products, create_product, get_all_products_no_pagination, get_system_in_movements_by_product, search_products_by_term, update_product, delete_product, get_product_by_id
from sqlalchemy.orm import Session
from app.models.groups import Product

class ProductService:
    @staticmethod
    def list_products(page,db):
        return get_all_active_products(page,db)
    
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
    def get_all_products_no_pagination_service(db):
        return get_all_products_no_pagination(db)
    
    @staticmethod
    def get_product_entry_history(product_id: int, page: int, db: Session):
        return  get_system_in_movements_by_product(product_id,page,db)