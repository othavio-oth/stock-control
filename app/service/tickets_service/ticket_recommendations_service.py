from datetime import datetime, date, time, timedelta
from typing import Optional, List, Dict

from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.models.tickets import Ticket, TicketProduct
from app.models.stockMovement import ClientStock, ClientLossHistory
from app.repository.tickets.tickets_repository import get_ticket_by_id

BUSINESS_START = time(7, 0)   # 07:00
BUSINESS_END   = time(20, 0)  # 20:00
BUSINESS_HOURS_PER_DAY = (datetime.combine(date.today(), BUSINESS_END) - datetime.combine(date.today(), BUSINESS_START)).seconds / 3600.0  # 13.0

def _clip_to_business_window(dt: datetime) -> Optional[datetime]:
    """Recorta um datetime para dentro do horário comercial (07:00–20:00).
    Se estiver fora, traz para a borda mais próxima dentro do mesmo dia."""
    day_start = datetime.combine(dt.date(), BUSINESS_START)
    day_end   = datetime.combine(dt.date(), BUSINESS_END)
    if dt < day_start:
        return day_start
    if dt > day_end:
        return day_end
    return dt

def _business_hours_between(start: datetime, end: datetime) -> float:
    """Horas úteis (07–20) entre start e end, somando dia a dia."""
    if end <= start:
        return 0.0

    total_hours = 0.0
    cur = start
    while cur.date() <= end.date():
        day_start = datetime.combine(cur.date(), BUSINESS_START)
        day_end   = datetime.combine(cur.date(), BUSINESS_END)

        # janela do dia atual
        wstart = max(cur, day_start) if cur.date() == start.date() else day_start
        wend   = min(end, day_end)   if cur.date() == end.date()   else day_end
        if wend > wstart:
            total_hours += (wend - wstart).total_seconds() / 3600.0

        # próximo dia
        cur = datetime.combine(cur.date() + timedelta(days=1), BUSINESS_START)

    return total_hours

def _get_last_approved_ticket_for_product_before(
    db: Session, cost_center_id: int, product_id: int, reference_order_date: date
) -> Optional[Ticket]:
    """Último ticket 'approved' do CC que contenha o produto, anterior ao order_date de referência (ciclo anterior)."""
    return (
        db.query(Ticket)
        .join(TicketProduct, TicketProduct.ticket_id == Ticket.id)
        .filter(
            Ticket.cost_center_id == cost_center_id,
            Ticket.status == "approved",
            Ticket.order_date < reference_order_date,
            TicketProduct.product_id == product_id,
        )
        .order_by(Ticket.order_date.desc())
        .first()
    )

def _get_ticket_qty_for_product(db: Session, ticket_id: int, product_id: int) -> int:
    tp = (
        db.query(TicketProduct)
        .filter(TicketProduct.ticket_id == ticket_id, TicketProduct.product_id == product_id)
        .first()
    )
    return int(tp.quantity_ordered) if tp else 0

def _get_client_stock(db: Session, cost_center_id: int, product_id: int) -> int:
    cs = (
        db.query(ClientStock)
        .filter(ClientStock.cost_center_id == cost_center_id, ClientStock.product_id == product_id)
        .first()
    )
    return int(cs.quantity) if cs else 0

def _get_losses_between(db: Session, cost_center_id: int, product_id: int, start_d: date, end_d: date) -> int:
    total = (
        db.query(func.coalesce(func.sum(ClientLossHistory.lost_quantity), 0))
        .filter(
            ClientLossHistory.cost_center_id == cost_center_id,
            ClientLossHistory.product_id == product_id,
            ClientLossHistory.date >= start_d,
            ClientLossHistory.date <= end_d,
        )
        .scalar()
    )
    return int(total or 0)

def get_daily_sales_avg_for_ticket(
    db: Session, ticket_id: int, evaluation_time: Optional[datetime] = None
) -> List[Dict]:
    """
    Para cada produto do ticket atual, calcula a média de vendas (por hora e por dia),
    considerando:
      - início: 07:00 do dia seguinte ao order_date do ÚLTIMO ticket aprovado que tinha o produto (ciclo anterior)
      - fim: horário em que o resultado de vendas foi registrado (evaluation_time) OU agora
      - horário comercial 07:00–20:00
      - vendido = (qtd enviada no ticket anterior) - (estoque atual do cliente) - (perdas no período)
    Retorna uma lista de dicts com métricas por produto.
    """
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        raise ValueError("Ticket não encontrado")

    cost_center_id = ticket.cost_center_id
    evaluation_time = evaluation_time or datetime.now()

    # recorta evaluation_time para janela comercial do dia
    evaluation_time = _clip_to_business_window(evaluation_time)

    results = []
    for tp in ticket.products:
        product_id = tp.product_id

        # 1) último ticket aprovado (ciclo anterior) que continha este produto
        last_ticket = _get_last_approved_ticket_for_product_before(
            db, cost_center_id, product_id, ticket.order_date
        )
        if not last_ticket:
            results.append({
                "product_id": product_id,
                "status": "sem_ticket_anterior",
                "avg_per_hour": 0.0,
                "avg_per_day": 0.0,
                "period_hours": 0.0,
                "notes": "Não foi encontrado ticket aprovado anterior para este produto."
            })
            continue

        # 2) início do período: 07:00 do dia seguinte ao order_date do último ticket
        start_dt = datetime.combine(last_ticket.order_date + timedelta(days=1), BUSINESS_START)

        # 3) fim do período = evaluation_time (já recortado para horário comercial)
        if not evaluation_time or evaluation_time <= start_dt:
            results.append({
                "product_id": product_id,
                "status": "periodo_invalido",
                "avg_per_hour": 0.0,
                "avg_per_day": 0.0,
                "period_hours": 0.0,
                "notes": "Fim do período não ultrapassa o início."
            })
            continue

        # 4) quantidade enviada no ticket anterior para este produto
        sent_qty = _get_ticket_qty_for_product(db, last_ticket.id, product_id)

        # 5) estoque atual do cliente (cost center) para este produto
        current_stock = _get_client_stock(db, cost_center_id, product_id)

        # 6) perdas no período (por dia)
        losses = _get_losses_between(
            db, cost_center_id, product_id, start_dt.date(), evaluation_time.date()
        )

        # 7) vendido por inferência (sem precisar de primeira/última venda)
        sold_qty = max(sent_qty - current_stock - losses, 0)

        # 8) horas úteis no período
        period_hours = _business_hours_between(start_dt, evaluation_time)

        if period_hours <= 0:
            avg_per_hour = 0.0
            avg_per_day = 0.0
        else:
            avg_per_hour = sold_qty / period_hours
            avg_per_day = avg_per_hour * BUSINESS_HOURS_PER_DAY  # “por dia” (13h)

        results.append({
            "product_id": product_id,
            "last_ticket_id": last_ticket.id,
            "start": start_dt.isoformat(),
            "end": evaluation_time.isoformat(),
            "period_hours": round(period_hours, 4),
            "sent_qty_prev_cycle": int(sent_qty),
            "current_client_stock": int(current_stock),
            "losses_in_period": int(losses),
            "inferred_sold_qty": int(sold_qty),
            "avg_per_hour": round(avg_per_hour, 6),
            "avg_per_day": round(avg_per_day, 6),
            "status": "ok"
        })

    return results

def _get_last_approved_tickets_for_product_before(
    db: Session, cost_center_id: int, product_id: int, reference_order_date: date, limit: int
) -> List[Ticket]:
    """Lista dos últimos 'limit' tickets approved contendo o produto, anteriores à data de referência."""
    return (
        db.query(Ticket)
        .join(TicketProduct, TicketProduct.ticket_id == Ticket.id)
        .filter(
            Ticket.cost_center_id == cost_center_id,
            Ticket.status == "approved",
            Ticket.order_date < reference_order_date,
            TicketProduct.product_id == product_id,
        )
        .order_by(Ticket.order_date.desc())
        .limit(limit)
        .all()
    )

def get_daily_sales_avg_for_last_cycles(
    db: Session,
    ticket_id: int,
    max_cycles: int = 8,
    evaluation_time: Optional[datetime] = None
) -> Dict[int, List[Dict]]:
    """
    Para cada produto do ticket, retorna uma LISTA com as métricas para os últimos 'max_cycles'
    tickets aprovados que continham esse produto (ou menos, se não houver tantos).
    O fim do período é o evaluation_time (ou agora) recortado para a janela 07–20.
    Retorna: { product_id: [ { ...ciclo mais recente... }, { ...ciclo-2... }, ... ] }
    """
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        raise ValueError("Ticket não encontrado")

    cost_center_id = ticket.cost_center_id
    evaluation_time = _clip_to_business_window(evaluation_time or datetime.now())

    out: Dict[int, List[Dict]] = {}

    for tp in ticket.products:
        product_id = tp.product_id

        # últimos N tickets aprovados anteriores que tinham este produto
        prev_tickets = _get_last_approved_tickets_for_product_before(
            db, cost_center_id, product_id, ticket.order_date, limit=max_cycles
        )

        if not prev_tickets:
            out[product_id] = []
            continue

        cycles: List[Dict] = []
        for prev in prev_tickets:
            # início do ciclo = 07:00 do dia seguinte ao order_date do ticket anterior
            start_dt = datetime.combine(prev.order_date + timedelta(days=1), BUSINESS_START)

            if evaluation_time <= start_dt:
                # Se o eval_time não ultrapassa o início, não há horas úteis a acumular
                cycles.append({
                    "ticket_id": prev.id,
                    "start": start_dt.isoformat(),
                    "end": evaluation_time.isoformat(),
                    "period_hours": 0.0,
                    "sent_qty_prev_cycle": 0,
                    "current_client_stock": _get_client_stock(db, cost_center_id, product_id),
                    "losses_in_period": 0,
                    "inferred_sold_qty": 0,
                    "avg_per_hour": 0.0,
                    "avg_per_day": 0.0,
                    "status": "periodo_invalido",
                })
                continue

            sent_qty = _get_ticket_qty_for_product(db, prev.id, product_id)
            current_stock = _get_client_stock(db, cost_center_id, product_id)
            losses = _get_losses_between(db, cost_center_id, product_id, start_dt.date(), evaluation_time.date())

            sold_qty = max(sent_qty - current_stock - losses, 0)
            period_hours = _business_hours_between(start_dt, evaluation_time)

            if period_hours <= 0:
                avg_per_hour = 0.0
                avg_per_day = 0.0
            else:
                avg_per_hour = sold_qty / period_hours
                avg_per_day = avg_per_hour * BUSINESS_HOURS_PER_DAY

            cycles.append({
                "ticket_id": prev.id,
                "start": start_dt.isoformat(),
                "end": evaluation_time.isoformat(),
                "period_hours": round(period_hours, 4),
                "sent_qty_prev_cycle": int(sent_qty),
                "current_client_stock": int(current_stock),
                "losses_in_period": int(losses),
                "inferred_sold_qty": int(sold_qty),
                "avg_per_hour": round(avg_per_hour, 6),
                "avg_per_day": round(avg_per_day, 6),
                "status": "ok",
            })

        out[product_id] = cycles

    return out