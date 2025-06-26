from . import *

def get_all_products(db):
    return db.query(Product).order_by(Product.id).all()

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