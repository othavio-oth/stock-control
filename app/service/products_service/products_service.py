from app.repository.products.products_repository import get_all_products, create_product, update_product, delete_product, get_product_by_id
from sqlalchemy.orm import Session
from app.models.groups import Product

class ProductService:
    @staticmethod
    def list_products(page,db):
        return get_all_products(page,db)

    @staticmethod
    def create_product(db, product_data):
        return create_product(db, product_data)

    @staticmethod
    def edit_product(db, product_id, product_data):
        if not get_product_by_id(db, product_id):
            raise ValueError("Produto não encontrado.")
        return update_product(db, product_id, product_data)

    @staticmethod
    def remove_product(db, product_id):
        if not get_product_by_id(db, product_id):
            raise ValueError("Produto não encontrado.")
        return delete_product(db, product_id)