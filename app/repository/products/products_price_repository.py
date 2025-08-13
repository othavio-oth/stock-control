from sqlalchemy import and_, case, false, func, literal, or_
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Any, Dict, Iterable, Optional, List

from app.models.product import ProductPriceHistory

def create_price_history(db: Session, price_data: dict) -> ProductPriceHistory:
    price_history = ProductPriceHistory(**price_data)
    db.add(price_history)
    db.commit()
    db.refresh(price_history)
    return price_history

def get_current_prices_for_products_and_cc(
    db: Session,
    product_ids: Iterable[int],
    cost_center_id: int,
    chain_id: Optional[int],
) -> List[Dict[str, Any]]:
    """
    Retorna o preço vigente por produto respeitando prioridade:
      1) cost_center_id == X
      2) retail_chain_id == chain_id
      3) retail_chain_id IS NULL AND cost_center_id IS NULL
    Para cada product_id, entrega só o melhor preço.
    """

    product_ids = list({int(pid) for pid in product_ids})
    if not product_ids:
        return []

    # prioridade por linha
    priority = case(
        (ProductPriceHistory.cost_center_id == cost_center_id, 1),
        (
            and_(
                chain_id.is_not(None) if hasattr(chain_id, "is_not") else True,
                ProductPriceHistory.retail_chain_id == chain_id
            ),
            2,
        ),
        (
            and_(
                ProductPriceHistory.retail_chain_id.is_(None),
                ProductPriceHistory.cost_center_id.is_(None),
            ),
            3,
        ),
        else_=999,
    )

    # rótulo da fonte (opcional, útil para depurar UI)
    source = case(
        (ProductPriceHistory.cost_center_id == cost_center_id, literal("cost_center")),
        (ProductPriceHistory.retail_chain_id == chain_id, literal("retail_chain")),
        (
            and_(
                ProductPriceHistory.retail_chain_id.is_(None),
                ProductPriceHistory.cost_center_id.is_(None),
            ),
            literal("default"),
        ),
        else_=literal("unknown"),
    ).label("source")

    # Considera apenas preços ativos (end_date NULL) e apenas os produtos requisitados.
    # Usa ROW_NUMBER para pegar a linha de menor prioridade (1 melhor) por product_id.
    subq = (
        db.query(
            ProductPriceHistory.product_id.label("product_id"),
            ProductPriceHistory.price.label("price"),
            source,
            func.row_number()
            .over(
                partition_by=ProductPriceHistory.product_id,
                order_by=priority.asc()
            )
            .label("rn"),
        )
        .filter(
            ProductPriceHistory.end_date.is_(None),
            ProductPriceHistory.product_id.in_(product_ids),
            or_(
                ProductPriceHistory.cost_center_id == cost_center_id,
                ProductPriceHistory.retail_chain_id == chain_id if chain_id else false(),
                and_(
                    ProductPriceHistory.retail_chain_id.is_(None),
                    ProductPriceHistory.cost_center_id.is_(None),
                ),
            ),
        )
        .subquery()
    )

    rows = db.query(subq.c.product_id, subq.c.price, subq.c.source).filter(subq.c.rn == 1).all()

    # Monta dicionário final e garante produtos sem preço → None
    result_map: Dict[int, Dict[str, Any]] = {
        int(r.product_id): {"product_id": int(r.product_id), "price": float(r.price) if r.price is not None else None, "source": r.source}
        for r in rows
    }

    for pid in product_ids:
        result_map.setdefault(pid, {"product_id": pid, "price": None, "source": None})

    return list(result_map.values())

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