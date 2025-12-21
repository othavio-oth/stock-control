from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.models.product import ProductPriceHistory
from app.models.tickets import CostCenter
from app.repository.products.products_price_repository import create_price_history, delete_price_history, get_all_current, get_all_current_by_product, get_current_prices_for_products_and_cc
from app.schemas.products_schemas.product_price_schema import ProductPriceHistoryCreate, ProductPriceHistoryUpdate

class ProductPriceHistoryService:
    
    @staticmethod
    def get_all_current_prices_service(db: Session) -> list[ProductPriceHistory]:
        return get_all_current(db)

    @staticmethod
    def create_price_history_service(db: Session, data: ProductPriceHistoryCreate) -> ProductPriceHistory:
        if data.retail_chain_id and data.cost_center_id:
            raise ValueError("Apenas um dos campos: retail_chain_id ou cost_center_id pode ser informado")
        return create_price_history(db, data.model_dump())

    @staticmethod
    def get_current_prices_service_by_product(db: Session, product_id: int) -> list[ProductPriceHistory]:
        return get_all_current_by_product(db, product_id)
    
    @staticmethod
    def update_price_service(db: Session, price_id: int, data: ProductPriceHistoryUpdate) -> Optional[ProductPriceHistory]:
        current_price = db.query(ProductPriceHistory).filter(
            ProductPriceHistory.id == price_id,
            ProductPriceHistory.end_date.is_(None)  # Só preços ativos
        ).with_for_update().first()

        if not current_price:
            return None

        current_price.end_date = datetime.now()
        db.flush()  # Persiste imediatamente

        new_price_record = ProductPriceHistory(
            product_id=current_price.product_id,
            price=data.price,  # Único campo alterado
            retail_chain_id=current_price.retail_chain_id,
            cost_center_id=current_price.cost_center_id,
            start_date=datetime.now()  # end_date=NULL (implícito)
        )

        db.add(new_price_record)
        db.commit()
        db.refresh(new_price_record)
        return new_price_record
        

        
    @staticmethod
    def delete_price_service(db: Session, price_id: int) -> bool:
        return delete_price_history(db, price_id)
    
    
    @staticmethod
    def get_current_prices_batch_for_cost_center(
        db: Session,
        product_ids: List[int],
        cost_center_id: int,
    ) -> List[Dict[str, Any]]:
        cc = db.query(CostCenter).filter(CostCenter.id == cost_center_id).first()
        if not cc:
            return [{"product_id": pid, "price": None, "source": None} for pid in product_ids]

        chain_id = cc.retail_chain_id  # pode ser None
        return get_current_prices_for_products_and_cc(db, product_ids, cost_center_id, chain_id)