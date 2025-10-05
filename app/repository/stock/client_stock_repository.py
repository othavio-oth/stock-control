from typing import Iterable, List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import case, func
from app.models.stockMovement import ClientStock
from sqlalchemy.exc import IntegrityError


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



def update_client_stock_quantity(
    db: Session,
    cost_center_id: int,
    product_id: int,
    quantity: int,
    upsert: bool = True,
) -> dict:
    """
    Atualiza a quantidade de um único produto na client_stock.
    Se upsert=True, cria a linha se não existir.
    Retorna {"product_id": int, "quantity": int}.
    """
    if quantity < 0:
        raise ValueError("quantity não pode ser negativo")

    row = (
        db.query(ClientStock)
        .filter(
            ClientStock.cost_center_id == cost_center_id,
            ClientStock.product_id == product_id,
        )
        .with_for_update(of=ClientStock)  # evita race em concorrência
        .one_or_none()
    )

    if row is None:
        if not upsert:
            # nada a fazer; você pode lançar erro ou só retornar zero/plain
            return {"product_id": product_id, "quantity": 0}
        row = ClientStock(
            cost_center_id=cost_center_id,
            product_id=product_id,
            quantity=quantity,
        )
        db.add(row)
    else:
        row.quantity = quantity

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    return {"product_id": product_id, "quantity": row.quantity}