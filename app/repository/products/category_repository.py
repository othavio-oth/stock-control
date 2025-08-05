from app.models.product import Category
from . import *

def get_all_categories(db):
    return db.query(Category).order_by(Category.id).all()

def get_category_by_id(db, category_id):
    return db.query(Category).filter(Category.id == category_id).first()

def create_category(db, category):
    category = Category(**category.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def update_category(db, category_id, category_data):
    category = get_category_by_id(db, category_id)
    if category:
        for key, value in category_data.dict().items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
    return category

def delete_category(db, category_id):
    category = get_category_by_id(db, category_id)
    if category:
        db.delete(category)
        db.commit()
    return category