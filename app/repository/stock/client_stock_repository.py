from typing import Iterable, List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import case, func
from app.models.stockMovement import ClientStock, MovementType, StockMovement


def get_client_stock_by_cost_center(
    db: Session,
    cost_center_id: int,
    product_ids: Optional[Iterable[int]] = None,
    include_zero: bool = False,
) -> List[Dict[str, Any]]:


    ids: Optional[List[int]] = None
    if product_ids:
        ids = sorted({int(x) for x in product_ids if x is not None})

    signed_qty = case(
        (
            StockMovement.movement_type == MovementType.TO_CLIENT.value,
            StockMovement.quantity,                     # +
        ),
        (
            StockMovement.movement_type == MovementType.CLIENT_SALE.value,
            -StockMovement.quantity,                    # -
        ),
        (
            StockMovement.movement_type == MovementType.CLIENT_LOSS.value,
            -StockMovement.quantity,                    # -
        ),
        else_=0,
    )

    q = (
        db.query(
            StockMovement.product_id.label("product_id"),
            func.coalesce(func.sum(signed_qty), 0).label("quantity"),
        )
        .filter(StockMovement.cost_center_id == cost_center_id)
        .group_by(StockMovement.product_id)
    )

    if ids:
        q = q.filter(StockMovement.product_id.in_(ids))

    rows = q.all()
    result = [{"product_id": int(r.product_id), "quantity": int(r.quantity)} for r in rows]

    # include_zero: garante zeros para ids solicitados que não apareceram
    if include_zero and ids:
        found = {r["product_id"] for r in result}
        for pid in ids:
            if pid not in found:
                result.append({"product_id": pid, "quantity": 0})

    return result