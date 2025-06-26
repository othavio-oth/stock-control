from . import *

def get_all_stock_products(db):
    return db.query(StockProducts).order_by(StockProducts.id).all()

def get_stock_product_by_id(db, stock_product_id):
    return db.query(StockProducts).filter(StockProducts.id == stock_product_id).first()

def create_stock_product(db, stock_product_data):
    stock_product = StockProducts(**stock_product_data.dict())
    db.add(stock_product)
    db.commit()
    db.refresh(stock_product)
    return stock_product

def update_stock_product(db, stock_product_id, stock_product_data):
    stock_product = get_stock_product_by_id(db, stock_product_id)
    if stock_product:
        for key, value in stock_product_data.dict().items():
            setattr(stock_product, key, value)
        db.commit()
        db.refresh(stock_product)
    return stock_product

def delete_stock_product(db, stock_product_id):
    stock_product = get_stock_product_by_id(db, stock_product_id)
    if stock_product:
        db.delete(stock_product)
        db.commit()
    return stock_product


def get_all_stock_products_history(db):
    return db.query(StockProductsHistory).order_by(StockProductsHistory.id).all()

def get_stock_product_history_by_id(db, stock_product_history_id):
    return db.query(StockProductsHistory).filter(StockProductsHistory.id == stock_product_history_id).first()

def create_stock_product_history(db, stock_product_history_data):
    stock_product_history = StockProductsHistory(**stock_product_history_data.dict())
    db.add(stock_product_history)
    db.commit()
    db.refresh(stock_product_history)
    return stock_product_history

def update_stock_product_history(db, stock_product_history_id, stock_product_history_data):
    stock_product_history = get_stock_product_history_by_id(db, stock_product_history_id)
    if stock_product_history:
        for key, value in stock_product_history_data.dict().items():
            setattr(stock_product_history, key, value)
        db.commit()
        db.refresh(stock_product_history)
    return stock_product_history

def delete_stock_product_history(db, stock_product_history_id):
    stock_product_history = get_stock_product_history_by_id(db, stock_product_history_id)
    if stock_product_history:
        db.delete(stock_product_history)
        db.commit()
    return stock_product_history