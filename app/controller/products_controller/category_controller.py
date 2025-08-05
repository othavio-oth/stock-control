from app.service.products_service.categories_service import CategoryService
from . import *

def list_categories(db):
    return CategoryService.list_categories(db)

def create_category(category_data, db):
    return CategoryService.create_category(db, category_data)

def edit_category(category_id, category_data, db):
    return CategoryService.edit_category(db, category_id, category_data)

def delete_category(category_id, db):
    return CategoryService.remove_category(db, category_id)