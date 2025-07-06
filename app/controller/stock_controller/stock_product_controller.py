from . import *

# Controller for StockProducts
def list_stock_products(db):
    return StockProductService.list_stock_products(db)

def create_stock_product(stock_product_data, db):
    logging.info(f"StockProduct created: {stock_product_data}")
    return StockProductService.create_stock_product(db, stock_product_data)

def edit_stock_product(stock_product_id, stock_product_data, db):
    return StockProductService.edit_stock_product(db, stock_product_id, stock_product_data)

def delete_stock_product(stock_product_id, db):
    return StockProductService.remove_stock_product(db, stock_product_id)

# Controller for StockProductsHistory
def list_stock_products_history(db):
    return StockProductHistoryService.list_stock_products_history(db)

def create_stock_product_history(stock_product_history_data, db):
    logging.info(f"StockProductHistory created: {stock_product_history_data}")
    return StockProductHistoryService.create_stock_product_history(db, stock_product_history_data)

def edit_stock_product_history(stock_product_history_id, stock_product_history_data, db):
    return StockProductHistoryService.edit_stock_product_history(db, stock_product_history_id, stock_product_history_data)

def delete_stock_product_history(stock_product_history_id, db):
    return StockProductHistoryService.remove_stock_product_history(db, stock_product_history_id)