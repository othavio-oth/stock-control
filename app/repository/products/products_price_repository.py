from sqlalchemy import or_
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List

from app.models.product import ProductPriceHistory

def create_price_history(db: Session, price_data: dict) -> ProductPriceHistory:
    price_history = ProductPriceHistory(**price_data)
    db.add(price_history)
    db.commit()
    db.refresh(price_history)
    return price_history

def get_current_by_product_and_entity(
    db: Session,
    product_id: int,
    retail_chain_id: Optional[int] = None,
    cost_center_id: Optional[int] = None
) -> Optional[ProductPriceHistory]:
    query = db.query(ProductPriceHistory).filter(
        ProductPriceHistory.product_id == product_id,
        ProductPriceHistory.end_date.is_(None))
    
    if retail_chain_id:
        query = query.filter(ProductPriceHistory.retail_chain_id == retail_chain_id)
    elif cost_center_id:
        query = query.filter(ProductPriceHistory.cost_center_id == cost_center_id)
    
    return query.first()

def get_all_current_by_product(db: Session, product_id: int) -> List[ProductPriceHistory]:
    return db.query(ProductPriceHistory).filter(
        ProductPriceHistory.product_id == product_id,
        ProductPriceHistory.end_date.is_(None)
    ).all()
    
def get_all_current(db: Session) -> List[ProductPriceHistory]:
    return db.query(ProductPriceHistory).filter(
        ProductPriceHistory.end_date.is_(None)
    ).all()

def close_current_price(db: Session, product_id: int, retail_chain_id: int = None, cost_center_id: int = None) -> bool:
    """Encerra o preço atual definindo end_date como agora"""
    current_price = db.query(ProductPriceHistory).filter(
        ProductPriceHistory.product_id == product_id,
        ProductPriceHistory.end_date.is_(None),
        or_(
            ProductPriceHistory.retail_chain_id == retail_chain_id,
            ProductPriceHistory.cost_center_id == cost_center_id
        )
    ).first()
    
    if current_price:
        current_price.end_date = datetime.now()
        db.commit()
        return True
    return False

def create_new_price(db: Session, product_id: int, price: float, retail_chain_id: int = None, cost_center_id: int = None) -> ProductPriceHistory:
    """Cria um novo registro de preço"""
    new_price = ProductPriceHistory(
        product_id=product_id,
        price=price,
        retail_chain_id=retail_chain_id,
        cost_center_id=cost_center_id,
        start_date=datetime.now()
    )
    db.add(new_price)
    db.commit()
    db.refresh(new_price)
    return new_price

def delete_price_history(db: Session, price_id: int) -> bool:
    price_history = db.query(ProductPriceHistory).filter_by(id=price_id).first()
    if price_history:
        db.delete(price_history)
        db.commit()
        return True
    return False

def get_price_history_by_id(db: Session, price_id: int) -> Optional[ProductPriceHistory]:
    return db.query(ProductPriceHistory).filter_by(id=price_id).first()