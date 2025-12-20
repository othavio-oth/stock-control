from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.product import ShelfPrice


def create_shelf_price(db: Session, data: dict) -> ShelfPrice:
    shelf_price = ShelfPrice(**data)
    db.add(shelf_price)
    db.commit()
    db.refresh(shelf_price)
    return shelf_price


def list_shelf_prices(
    db: Session,
    *,
    product_id: Optional[int] = None,
    cost_center_id: Optional[int] = None,
    retail_chain_id: Optional[int] = None,
) -> List[ShelfPrice]:
    query = db.query(ShelfPrice)
    if product_id is not None:
        query = query.filter(ShelfPrice.product_id == product_id)
    if cost_center_id is not None:
        query = query.filter(ShelfPrice.cost_center_id == cost_center_id)
    if retail_chain_id is not None:
        query = query.filter(ShelfPrice.retail_chain_id == retail_chain_id)
    return query.order_by(ShelfPrice.start_date.desc(), ShelfPrice.id.desc()).all()


def get_shelf_price_by_id(db: Session, shelf_price_id: int) -> Optional[ShelfPrice]:
    return db.query(ShelfPrice).filter(ShelfPrice.id == shelf_price_id).first()


def update_shelf_price(db: Session, shelf_price_id: int, data: dict) -> Optional[ShelfPrice]:
    shelf_price = get_shelf_price_by_id(db, shelf_price_id)
    if not shelf_price:
        return None

    for key, value in data.items():
        setattr(shelf_price, key, value)

    db.commit()
    db.refresh(shelf_price)
    return shelf_price


def delete_shelf_price(db: Session, shelf_price_id: int) -> bool:
    shelf_price = get_shelf_price_by_id(db, shelf_price_id)
    if not shelf_price:
        return False

    db.delete(shelf_price)
    db.commit()
    return True
