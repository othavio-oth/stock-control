from typing import Iterable, List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import case, func
from app.models.stockMovement import ClientStock


from typing import Any, Dict, Iterable, List, Optional
from sqlalchemy.orm import Session
from app.models.stockMovement import ClientStock

def get_client_stock_by_cost_center(
    db: Session,
    cost_center_id: int,
    product_ids: Optional[Iterable[int]] = None,
    include_zero: bool = False,
) -> List[Dict[str, Any]]:

    ids: Optional[List[int]] = None
    if product_ids:
        ids = sorted({int(x) for x in product_ids if x is not None})

    q = (
        db.query(ClientStock.product_id, ClientStock.quantity)
        .filter(ClientStock.cost_center_id == cost_center_id)
    )
    if ids:
        q = q.filter(ClientStock.product_id.in_(ids))

    rows = q.all()

    # Monta resultado diretamente do que está em client_stock
    result = [{"product_id": int(pid), "quantity": int(qty)} for pid, qty in rows]

    # include_zero: garante zeros para ids solicitados que não apareceram
    if include_zero and ids:
        found = {r["product_id"] for r in result}
        for pid in ids:
            if pid not in found:
                result.append({"product_id": pid, "quantity": 0})

    return result
