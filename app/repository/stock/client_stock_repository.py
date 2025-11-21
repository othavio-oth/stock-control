from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Sequence
from sqlalchemy.orm import Session
from sqlalchemy import case, func
from sqlalchemy.exc import IntegrityError

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


def sync_client_stock_from_snapshot(
    db: Session,
    *,
    cost_center_id: int,
    product_quantities: Iterable[dict],
    observed_at: Optional[datetime],
) -> None:
    """
    Ajusta client_stock para refletir as quantidades observadas em uma visita
    de inventário (InventoryVisit).
    """
    qty_map: Dict[int, int] = {}
    for entry in product_quantities:
        try:
            pid = int(entry["product_id"])
            qty = int(entry.get("stock_quantity", 0) or 0)
        except (KeyError, TypeError, ValueError):
            continue
        qty_map[pid] = qty

    if not qty_map:
        return

    existing_rows = (
        db.query(ClientStock)
        .filter(
            ClientStock.cost_center_id == cost_center_id,
            ClientStock.product_id.in_(list(qty_map.keys())),
        )
        .with_for_update(of=ClientStock)
        .all()
    )
    existing_map = {row.product_id: row for row in existing_rows}

    timestamp = observed_at or datetime.now(timezone.utc)

    for pid, qty in qty_map.items():
        row = existing_map.get(pid)
        if row:
            row.quantity = qty
            row.last_observed_at = timestamp
            row.last_zeroed_at = timestamp if qty == 0 else None
        else:
            db.add(
                ClientStock(
                    cost_center_id=cost_center_id,
                    product_id=pid,
                    quantity=qty,
                    last_observed_at=timestamp,
                    last_zeroed_at=(timestamp if qty == 0 else None),
                )
            )


def zero_absent_client_stock_entries(
    db: Session,
    *,
    cost_center_id: int,
    observed_product_ids: Sequence[int] | None,
    zeroed_at: Optional[datetime],
) -> None:
    """
    Define quantity=0 para todos os produtos do cost center que não foram
    observados na visita e registra o momento do zeramento.
    """
    normalized_ids = sorted({int(pid) for pid in observed_product_ids or [] if pid is not None})

    q = (
        db.query(ClientStock)
        .filter(ClientStock.cost_center_id == cost_center_id)
    )
    if normalized_ids:
        q = q.filter(~ClientStock.product_id.in_(normalized_ids))

    rows = q.with_for_update(of=ClientStock).all()
    timestamp = zeroed_at or datetime.now(timezone.utc)

    for row in rows:
        row.quantity = 0
        row.last_observed_at = timestamp
        row.last_zeroed_at = timestamp
