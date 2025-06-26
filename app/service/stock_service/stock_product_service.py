from app.models.tickets import StockProducts, StockProductsHistory, Ticket
from app.repository.stock.stock_product_repository import create_stock_product, get_all_stock_products, get_stock_product_by_id, update_stock_product, delete_stock_product, get_all_stock_products_history, get_stock_product_history_by_id, create_stock_product_history, update_stock_product_history, delete_stock_product_history

class StockProductService:
    @staticmethod
    def list_stock_products(db):
        return get_all_stock_products(db)

    @staticmethod
    def create_stock_product(db, stock_product_data):
        existing_product = db.query(StockProducts).filter(StockProducts.name == stock_product_data.name).first()
        if existing_product:
            raise ValueError("Produto com este nome já existe.")
        return create_stock_product(db, stock_product_data)

    @staticmethod
    def edit_stock_product(db, stock_product_id, stock_product_data):
        if not get_stock_product_by_id(db, stock_product_id):
            raise ValueError("Produto não encontrado.")
        return update_stock_product(db, stock_product_id, stock_product_data)

    @staticmethod
    def remove_stock_product(db, stock_product_id):
        if not get_stock_product_by_id(db, stock_product_id):
            raise ValueError("Produto não encontrado.")
        return delete_stock_product(db, stock_product_id)

# Service Layer for StockProductsHistory
class StockProductHistoryService:
    @staticmethod
    def list_stock_products_history(db):
        return get_all_stock_products_history(db)

    @staticmethod
    def create_stock_product_history(db, stock_product_history_data):
        return create_stock_product_history(db, stock_product_history_data)

    @staticmethod
    def edit_stock_product_history(db, stock_product_history_id, stock_product_history_data):
        if not get_stock_product_history_by_id(db, stock_product_history_id):
            raise ValueError("Histórico de produto não encontrado.")
        return update_stock_product_history(db, stock_product_history_id, stock_product_history_data)

    @staticmethod
    def remove_stock_product_history(db, stock_product_history_id):
        if not get_stock_product_history_by_id(db, stock_product_history_id):
            raise ValueError("Histórico de produto não encontrado.")
        return delete_stock_product_history(db, stock_product_history_id)