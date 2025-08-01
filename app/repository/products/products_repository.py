from sqlalchemy import or_
from . import *

def get_all_products(page,db):
    page_size = 20
    offset = (page - 1) * page_size
    total = db.query(Product).count()
    products = db.query(Product).order_by(Product.id).offset(offset).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": products,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

def get_product_by_id(db, product_id):
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db, product_data):
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db, product_id, product_data):
    product = get_product_by_id(db, product_id)
    if product:
        for key, value in product_data.dict().items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
    return product

def delete_product(db, product_id):
    product = get_product_by_id(db, product_id)
    if product:
        db.delete(product)
        db.commit()
    return product


def search_products_by_term( search_term: str,page:int,db: Session):
    page_size = 20
    offset = (page - 1) * page_size
    base_query = db.query(Product).filter(
            or_(
                Product.id == int(search_term) if search_term.isdigit() else False,
                Product.description.ilike(f"%{search_term}%"),
            )
        )
    total = base_query.count()
    total_pages = (total + page_size - 1) // page_size

    tickets = base_query.offset(offset).limit(page_size).all()
    return {
    "items": tickets,
    "total": total,
    "page": page,
    "page_size": page_size,
    "total_pages": total_pages
    }