from datetime import date, datetime, timedelta
from typing import Dict, List
from sqlalchemy.orm import Session

from app.repository.stock.stock_movement_repository import (
    get_ticket_approved_at,
    get_existing_sales_days,
    upsert_sales_for_day,
    create_client_sale_movement,
    get_or_create_client_stock_for_update,
    decrement_client_stock,
)
from app.schemas.stock_schemas.stock_movement_schema import ClientSalesAnchoredDTO

def _daterange(start: date, end: date) -> List[date]:
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]

def _build_allocation_map(days: List[date], total: int, strategy: str) -> Dict[date, int]:
    """
    Distribui 'total' entre 'days' garantindo soma exata:
    - even/front: reparte igual e coloca as sobras nos dias mais antigos
    - back: reparte igual e coloca as sobras nos dias mais recentes
    """
    if not days or total <= 0:
        return {d: 0 for d in days}

    base = total // len(days)
    rest = total % len(days)

    ordered = list(days)
    if strategy == "back":
        ordered = list(reversed(days))  # sobras nos mais recentes
    # "even" e "front": sobras nos mais antigos (ordem natural)

    alloc = {d: base for d in days}
    for d in ordered[:rest]:
        alloc[d] += 1
    return alloc

class ProductSalesService:


    @staticmethod
    @staticmethod
    def register_client_sales_anchored_to_ticket(db: Session, payload: ClientSalesAnchoredDTO):
        """
        Registra vendas do cliente ancoradas ao ticket apenas pela DATA:
        - start_date = ticket.approved_at + 1
        - end_date   = registration_dt.date() (ou hoje)
        - distribui total_sold somente em dias ainda não lançados (idempotente)
        - grava ClientSalesHistory por dia + StockMovement CLIENT_SALE por dia
        - baixa o ClientStock pelo total aplicado
        """
        # 1) Âncora temporal via ticket
        approved_at = get_ticket_approved_at(db, payload.ticket_id)
        if not approved_at:
            raise ValueError("Ticket não possui 'approved_at' ou não foi encontrado.")

        start_date = approved_at + timedelta(days=1)
        end_date = (payload.registration_dt or datetime.now()).date()
        today = datetime.now().date()
        if end_date > today:
            end_date = today

        if start_date > end_date:
            return {"message": "Não há dias a registrar após a aprovação."}

        if payload.total_sold <= 0:
            return {"message": "Nada a lançar (total_sold <= 0)."}

        # 2) Evitar duplicidade: só usa dias “livres”
        all_days = _daterange(start_date, end_date)
        used_days = get_existing_sales_days(db, payload.cost_center_id, payload.product_id, start_date, end_date)
        free_days = [d for d in all_days if d not in used_days]
        if not free_days:
            return {"message": "Período já lançado anteriormente (nenhum dia livre para distribuição)."}

        allocation = _build_allocation_map(free_days, payload.total_sold, payload.distribute)

        # 3) Estoque do cliente (lock + validação)
        cs = get_or_create_client_stock_for_update(db, payload.cost_center_id, payload.product_id)
        total_planned = sum(allocation.values())
        if (not payload.allow_negative_client_stock) and cs.quantity < total_planned:
            raise ValueError(f"Estoque insuficiente no cliente. Em estoque: {cs.quantity}, vendido: {total_planned}")

        # 4) Persistência por dia (upsert + movement)
        total_applied = 0
        for day, qty in allocation.items():
            if qty <= 0:
                continue
            upsert_sales_for_day(db, payload.cost_center_id, payload.product_id, day, qty)
            created_at = datetime.combine(day, datetime.min.time())
            create_client_sale_movement(db, payload.product_id, payload.cost_center_id, qty, created_at)
            total_applied += qty

        # 5) Baixa no estoque do cliente e commit
        decrement_client_stock(cs, total_applied, payload.allow_negative_client_stock)
        db.commit()

        return {
            "ticket_id": payload.ticket_id,
            "product_id": payload.product_id,
            "cost_center_id": payload.cost_center_id,
            "period_used": {"start_date": str(start_date), "end_date": str(end_date)},
            "distributed_strategy": payload.distribute,
            "total_sold": payload.total_sold,
            "applied": total_applied,
        }
