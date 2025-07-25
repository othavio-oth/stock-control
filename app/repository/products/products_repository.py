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