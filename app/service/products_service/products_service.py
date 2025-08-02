from fastapi import HTTPException
from app.repository.products.products_repository import get_all_products, create_product, search_products_by_term, update_product, delete_product, get_product_by_id
from sqlalchemy.orm import Session
from app.models.groups import Product

class ProductService:
    @staticmethod
    def list_products(page,db):
        return get_all_products(page,db)
    
    @staticmethod
    def get_product(db, product_id):
        product = get_product_by_id(db, product_id)
        if not product:
            raise HTTPException(404,"Produto não encontrado.")
        return product
    
    @staticmethod
    def remove_product(db, product_id):
        product = ProductService.get_product(db, product_id)
        return delete_product(db, product)

    @staticmethod
    def create_product(db, product_data):
        return create_product(db, product_data)

    @staticmethod
    def edit_product(db, product_id, product_data):
        if not get_product_by_id(db, product_id):
            raise ValueError("Produto não encontrado.")
        return update_product(db, product_id, product_data)

    
    @staticmethod
    def search_products(term,page, db):
        return search_products_by_term(term,page, db)