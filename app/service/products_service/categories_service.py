

from app.models.product import Category
from app.repository.products.category_repository import create_category, delete_category, get_all_categories, get_category_by_id, update_category


class CategoryService:
    @staticmethod
    def list_categories(db):
        return get_all_categories(db)

    @staticmethod
    def create_category(db, category_data):
        existing_type = db.query(Category).filter(Category.name == category_data.name).first()
        if existing_type:
            raise ValueError("Tipo de Registro com este nome já existe.")
        return create_category(db, category_data)

    @staticmethod
    def edit_category(db, category_id, category_data):
        if not get_category_by_id(db, category_id):
            raise ValueError("Tipo de Registro não encontrado.")
        return update_category(db, category_id, category_data)

    @staticmethod
    def remove_category(db, category_id):
        if not get_category_by_id(db, category_id):
            raise ValueError("Tipo de Registro não encontrado.")
        return delete_category(db, category_id)