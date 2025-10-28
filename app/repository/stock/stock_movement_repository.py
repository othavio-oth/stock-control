from collections import defaultdict
from time import time
from typing import Any, Dict, List, Optional, Sequence, Set
from sqlalchemy.orm import Session
from sqlalchemy import case, extract, func
from app.models.tickets import Ticket, TicketProduct
from app.schemas.stock_schemas.stock_movement_schema import  StockMovementLost, TotalProductStockResponse
from app.models.stockMovement import ClientLossHistory, ClientSalesHistory, ClientStock, MovementType, InventoryStock
from app.models.product import Supplier
from sqlalchemy.orm import joinedload
from sqlalchemy import and_ 
from datetime import datetime, timedelta
from app.models.stockMovement import StockMovement
from app.models.product import Product

from sqlalchemy.orm import Session
from datetime import date
from app.models.tickets import CostCenter


BUSINESS_START = 7   # 07:00
BUSINESS_END   = 20  # 20:00 (exclusivo, i.e., atÃ© 19:59:59)

def process_stock_movement(db: Session, movement: StockMovement):
    """
    Atualiza estoques do INVENTÃRIO e/ou do CLIENTE conforme o tipo de movimento.
    Regras:
      - SUPPLIER_PURCHASE: inventÃ¡rio ++ (exige supplier_id)
      - SUPPLIER_LOSS: inventÃ¡rio --
      - TO_CLIENT: inventÃ¡rio -- e cliente ++
      - CLIENT_SALE: cliente -- (+ histÃ³rico de venda)
      - CLIENT_LOSS: cliente -- (+ histÃ³rico de perda)
    """
    # -------- INVENTÃRIO (fornecedor) --------
    if movement.movement_type in [
        MovementType.SUPPLIER_PURCHASE,
        MovementType.SUPPLIER_LOSS,
        MovementType.TO_CLIENT,
    ]:
        if movement.movement_type == MovementType.SUPPLIER_PURCHASE and not movement.supplier_id:
            raise ValueError("MovimentaÃ§Ãµes SUPPLIER_PURCHASE exigem supplier_id.")

        supplier_stock = (
            db.query(InventoryStock)
              .filter_by(product_id=movement.product_id)
              .with_for_update()
              .first()
        )
        if not supplier_stock:
            supplier_stock = InventoryStock(product_id=movement.product_id, quantity=0)
            db.add(supplier_stock)
            db.flush()

        if movement.movement_type == MovementType.SUPPLIER_PURCHASE:
            supplier_stock.quantity += movement.quantity
        else:
            # SUPPLIER_LOSS ou TO_CLIENT â†’ debita inventÃ¡rio
            if supplier_stock.quantity < movement.quantity:
                raise ValueError(
                    f"Estoque do inventÃ¡rio insuficiente: "
                    f"disp={supplier_stock.quantity}, req={movement.quantity}"
                )
            supplier_stock.quantity -= movement.quantity

    # -------- CLIENTE (cost center) --------
    if movement.cost_center_id:
        client_stock = (
            db.query(ClientStock)
              .filter_by(product_id=movement.product_id,
                         cost_center_id=movement.cost_center_id)
              .with_for_update()
              .first()
        )
        if not client_stock:
            client_stock = ClientStock(
                product_id=movement.product_id,
                cost_center_id=movement.cost_center_id,
                quantity=0
            )
            db.add(client_stock)
            db.flush()

        if movement.movement_type == MovementType.TO_CLIENT:
            client_stock.quantity += movement.quantity

        elif movement.movement_type == MovementType.CLIENT_SALE:
            if client_stock.quantity < movement.quantity:
                raise ValueError(
                    f"Estoque do cliente insuficiente para venda: "
                    f"disp={client_stock.quantity}, req={movement.quantity}"
                )
            client_stock.quantity -= movement.quantity

            # HistÃ³rico de vendas (por dia)
            sales_record = (
                db.query(ClientSalesHistory)
                  .filter_by(product_id=movement.product_id,
                             cost_center_id=movement.cost_center_id,
                             date=(movement.created_at.date() if movement.created_at else date.today()))
                  .first()
            )
            if not sales_record:
                sales_record = ClientSalesHistory(
                    product_id=movement.product_id,
                    cost_center_id=movement.cost_center_id,
                    date=(movement.created_at.date() if movement.created_at else date.today()),
                    sold_quantity=0
                )
                db.add(sales_record)
            sales_record.sold_quantity += movement.quantity

        elif movement.movement_type == MovementType.CLIENT_LOSS:
            if client_stock.quantity < movement.quantity:
                raise ValueError(
                    f"Estoque do cliente insuficiente para perda: "
                    f"disp={client_stock.quantity}, req={movement.quantity}"
                )
            client_stock.quantity -= movement.quantity

            # HistÃ³rico de perdas (por dia)
            loss_record = (
                db.query(ClientLossHistory)
                  .filter_by(product_id=movement.product_id,
                             cost_center_id=movement.cost_center_id,
                             date=(movement.created_at.date() if movement.created_at else date.today()))
                  .first()
            )
            if not loss_record:
                loss_record = ClientLossHistory(
                    product_id=movement.product_id,
                    cost_center_id=movement.cost_center_id,
                    date=(movement.created_at.date() if movement.created_at else date.today()),
                    lost_quantity=0,
                    reason="Perda registrada"
                )
                db.add(loss_record)
            loss_record.lost_quantity += movement.quantity

    db.commit()


def get_client_loss_history(
    db: Session,
    *,
    cost_center_id: int,
    product_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[ClientLossHistory]:
    """
    Retorna o histórico de perdas para um cost center, com filtros opcionais.
    """
    q = db.query(ClientLossHistory).filter(ClientLossHistory.cost_center_id == cost_center_id)

    if product_id is not None:
        q = q.filter(ClientLossHistory.product_id == product_id)
    if start_date is not None:
        q = q.filter(ClientLossHistory.date >= start_date)
    if end_date is not None:
        q = q.filter(ClientLossHistory.date <= end_date)

    return q.order_by(ClientLossHistory.date.asc()).all()


def get_client_sales_and_loss_history(
    db: Session,
    *,
    cost_center_id: int,
    product_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[Dict[str, Any]]:
    """
    Consolida vendas e perdas para um mesmo cost center, agrupadas por dia e produto.
    """
    sales_filters = [ClientSalesHistory.cost_center_id == cost_center_id]
    loss_filters = [ClientLossHistory.cost_center_id == cost_center_id]

    if product_id is not None:
        sales_filters.append(ClientSalesHistory.product_id == product_id)
        loss_filters.append(ClientLossHistory.product_id == product_id)
    if start_date is not None:
        sales_filters.append(ClientSalesHistory.date >= start_date)
        loss_filters.append(ClientLossHistory.date >= start_date)
    if end_date is not None:
        sales_filters.append(ClientSalesHistory.date <= end_date)
        loss_filters.append(ClientLossHistory.date <= end_date)

    sales_rows = (
        db.query(ClientSalesHistory)
        .filter(*sales_filters)
        .order_by(ClientSalesHistory.date.asc())
        .all()
    )
    loss_rows = (
        db.query(ClientLossHistory)
        .filter(*loss_filters)
        .order_by(ClientLossHistory.date.asc())
        .all()
    )

    combined: Dict[tuple[int, date], Dict[str, Any]] = {}

    for row in sales_rows:
        key = (row.product_id, row.date)
        if key not in combined:
            combined[key] = {
                "cost_center_id": row.cost_center_id,
                "product_id": row.product_id,
                "date": row.date,
                "sold_quantity": 0,
                "lost_quantity": 0,
                "previous_ticket_id": None,
                "previous_ticket_order_date": None,
                "previous_ticket_name": None,
                "previous_ticket_quantity": None,
            }
        combined[key]["sold_quantity"] += int(row.sold_quantity or 0)

    for row in loss_rows:
        key = (row.product_id, row.date)
        if key not in combined:
            combined[key] = {
                "cost_center_id": row.cost_center_id,
                "product_id": row.product_id,
                "date": row.date,
                "sold_quantity": 0,
                "lost_quantity": 0,
                "previous_ticket_id": None,
                "previous_ticket_order_date": None,
                "previous_ticket_name": None,
                "previous_ticket_quantity": None,
            }
        combined[key]["lost_quantity"] += int(row.lost_quantity or 0)

    if not combined:
        return []

    dates_by_product: Dict[int, List[date]] = defaultdict(list)
    for (product_id, day), _ in combined.items():
        dates_by_product[product_id].append(day)

    for product, days in dates_by_product.items():
        sorted_days = sorted(set(days))
        max_day = sorted_days[-1]
        ticket_rows = (
            db.query(
                Ticket.id.label("ticket_id"),
                Ticket.name.label("ticket_name"),
                Ticket.order_date.label("order_date"),
                TicketProduct.quantity_ordered.label("quantity_ordered"),
            )
            .join(TicketProduct, TicketProduct.ticket_id == Ticket.id)
            .filter(
                Ticket.cost_center_id == cost_center_id,
                TicketProduct.product_id == product,
                Ticket.status == "approved",
                Ticket.order_date < max_day,
            )
            .order_by(Ticket.order_date.asc(), Ticket.id.asc())
            .all()
        )
        if not ticket_rows:
            continue
        idx = 0
        last_ticket = None
        ticket_count = len(ticket_rows)
        for day in sorted_days:
            while idx < ticket_count and ticket_rows[idx].order_date < day:
                last_ticket = ticket_rows[idx]
                idx += 1
            if last_ticket and last_ticket.order_date < day:
                key = (product, day)
                combined[key]["previous_ticket_id"] = last_ticket.ticket_id
                combined[key]["previous_ticket_order_date"] = last_ticket.order_date
                combined[key]["previous_ticket_name"] = last_ticket.ticket_name
                combined[key]["previous_ticket_quantity"] = (
                    int(last_ticket.quantity_ordered) if last_ticket.quantity_ordered is not None else None
                )

    return sorted(combined.values(), key=lambda item: (item["product_id"], item["date"]))


def get_daily_sales_and_loss_grouped_by_cost_center(
    db: Session,
    *,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    cost_center_ids: Optional[Sequence[int]] = None,
    product_id: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Soma vendas e perdas por cost center/produto/dia, agrupando resultados por cost center.
    """
    sales_query = (
        db.query(
            ClientSalesHistory.cost_center_id,
            ClientSalesHistory.product_id,
            ClientSalesHistory.date,
            func.coalesce(func.sum(ClientSalesHistory.sold_quantity), 0).label("sold_quantity"),
        )
    )
    loss_query = (
        db.query(
            ClientLossHistory.cost_center_id,
            ClientLossHistory.product_id,
            ClientLossHistory.date,
            func.coalesce(func.sum(ClientLossHistory.lost_quantity), 0).label("lost_quantity"),
        )
    )

    if start_date is not None:
        sales_query = sales_query.filter(ClientSalesHistory.date >= start_date)
        loss_query = loss_query.filter(ClientLossHistory.date >= start_date)
    if end_date is not None:
        sales_query = sales_query.filter(ClientSalesHistory.date <= end_date)
        loss_query = loss_query.filter(ClientLossHistory.date <= end_date)
    if product_id is not None:
        sales_query = sales_query.filter(ClientSalesHistory.product_id == product_id)
        loss_query = loss_query.filter(ClientLossHistory.product_id == product_id)
    if cost_center_ids:
        sales_query = sales_query.filter(ClientSalesHistory.cost_center_id.in_(cost_center_ids))
        loss_query = loss_query.filter(ClientLossHistory.cost_center_id.in_(cost_center_ids))

    sales_rows = sales_query.group_by(
        ClientSalesHistory.cost_center_id,
        ClientSalesHistory.product_id,
        ClientSalesHistory.date,
    ).all()
    loss_rows = loss_query.group_by(
        ClientLossHistory.cost_center_id,
        ClientLossHistory.product_id,
        ClientLossHistory.date,
    ).all()

    if not sales_rows and not loss_rows:
        return []

    combined: Dict[int, Dict[tuple[int, date], Dict[str, Any]]] = defaultdict(dict)
    product_ids: Set[int] = set()
    cc_ids: Set[int] = set()

    for row in sales_rows:
        key = (row.product_id, row.date)
        bucket = combined[row.cost_center_id].setdefault(
            key,
            {
                "cost_center_id": row.cost_center_id,
                "product_id": row.product_id,
                "date": row.date,
                "sold_quantity": 0,
                "lost_quantity": 0,
            },
        )
        bucket["sold_quantity"] += int(row.sold_quantity or 0)
        product_ids.add(row.product_id)
        cc_ids.add(row.cost_center_id)

    for row in loss_rows:
        key = (row.product_id, row.date)
        bucket = combined[row.cost_center_id].setdefault(
            key,
            {
                "cost_center_id": row.cost_center_id,
                "product_id": row.product_id,
                "date": row.date,
                "sold_quantity": 0,
                "lost_quantity": 0,
            },
        )
        bucket["lost_quantity"] += int(row.lost_quantity or 0)
        product_ids.add(row.product_id)
        cc_ids.add(row.cost_center_id)

    product_names: Dict[int, str] = {}
    if product_ids:
        rows = (
            db.query(Product.id, Product.name)
            .filter(Product.id.in_(product_ids))
            .all()
        )
        product_names = {pid: name for pid, name in rows}

    cost_center_names: Dict[int, str] = {}
    if cc_ids:
        rows = (
            db.query(CostCenter.id, CostCenter.name)
            .filter(CostCenter.id.in_(cc_ids))
            .all()
        )
        cost_center_names = {cid: name for cid, name in rows}

    result: List[Dict[str, Any]] = []
    for cc_id, items in combined.items():
        entries = []
        for (product_id_value, day), payload in sorted(
            items.items(), key=lambda entry: (entry[0][1], entry[0][0])
        ):
            entries.append(
                {
                    "date": payload["date"],
                    "product_id": product_id_value,
                    "product_name": product_names.get(product_id_value),
                    "sold_quantity": payload["sold_quantity"],
                    "lost_quantity": payload["lost_quantity"],
                }
            )

        result.append(
            {
                "cost_center_id": cc_id,
                "cost_center_name": cost_center_names.get(cc_id),
                "results": entries,
            }
        )

    return sorted(
        result,
        key=lambda item: (
            (item["cost_center_name"] or "").lower(),
            item["cost_center_id"],
        ),
    )


def get_all_stock_movements(
    db: Session,
    movement_type: Optional[str] = None,
    product_id: Optional[int] = None,
):
    q = db.query(StockMovement)
    if product_id is not None:
        q = q.filter(StockMovement.product_id == product_id)
    if movement_type:
        try:
            # Aceita valor string (ex: "supplier_purchase") e converte p/ Enum
            mt = MovementType(movement_type)
        except Exception:
            # fallback: tenta comparar como string literal (caso já venha válido)
            mt = movement_type
        q = q.filter(StockMovement.movement_type == mt)
    return q.order_by(StockMovement.created_at.desc()).offset(0).limit(100).all()


def get_product_entries(
    db: Session,
    product_id: int,
    page: int = 1,
    page_size: int = 20,
):
    offset = (page - 1) * page_size
    base_q = (
        db.query(StockMovement)
        .options(joinedload(StockMovement.supplier))
        .filter(
            StockMovement.product_id == product_id,
            StockMovement.movement_type == MovementType.SUPPLIER_PURCHASE,
        )
        .order_by(StockMovement.created_at.desc())
    )
    total = base_q.count()
    items = base_q.offset(offset).limit(page_size).all()
    return total, items


def get_current_stock(db:Session):
    return db.query(InventoryStock).all()

def get_ticket_approved_at(db: Session, ticket_id: int) -> Optional[date]:
    row = db.query(Ticket.approved_at).filter(Ticket.id == ticket_id).first()
    return row[0] if row and row[0] else None

def get_existing_sales_days(
    db: Session,
    cost_center_id: int,
    product_id: int,
    start: date,
    end: date,
) -> Set[date]:
    """
    Retorna os dias que jÃ¡ possuem vendas registradas no intervalo [start, end].
    Ãštil para evitar duplicidade ao distribuir o total por dia.
    """
    rows = (
        db.query(ClientSalesHistory.date)
        .filter(
            ClientSalesHistory.cost_center_id == cost_center_id,
            ClientSalesHistory.product_id == product_id,
            ClientSalesHistory.date >= start,
            ClientSalesHistory.date <= end,
        )
        .all()
    )
    return {r[0] for r in rows}


def upsert_sales_for_day(
    db: Session,
    cost_center_id: int,
    product_id: int,
    d: date,
    qty: int,
) -> None:
    """
    Faz upsert da venda diÃ¡ria (somando ao que jÃ¡ existir no dia).
    """
    sales = (
        db.query(ClientSalesHistory)
        .filter_by(product_id=product_id, cost_center_id=cost_center_id, date=d)
        .first()
    )
    if not sales:
        sales = ClientSalesHistory(
            product_id=product_id,
            cost_center_id=cost_center_id,
            date=d,
            sold_quantity=0,
        )
        db.add(sales)
    sales.sold_quantity += qty


# â€”â€”â€” StockMovement â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”

def create_client_sale_movement(
    db: Session,
    product_id: int,
    cost_center_id: int,
    qty: int,
    created_at: datetime,
    product_unit_cost: Optional[float] = None,
) -> None:
    """
    Cria uma movimentaÃ§Ã£o do tipo CLIENT_SALE no dia da venda.
    """
    mv = StockMovement(
        product_id=product_id,
        quantity=qty,
        movement_type=MovementType.CLIENT_SALE,
        cost_center_id=cost_center_id,
        created_at=created_at,          # sobrescreve o server_default
        product_unit_cost=product_unit_cost,
    )
    db.add(mv)


# â€”â€”â€” ClientStock â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”

def get_or_create_client_stock_for_update(
    db: Session,
    cost_center_id: int,
    product_id: int,
) -> ClientStock:
    """
    Retorna o ClientStock com lock (FOR UPDATE). Cria com quantity=0 se nÃ£o existir.
    """
    cs = (
        db.query(ClientStock)
        .filter_by(product_id=product_id, cost_center_id=cost_center_id)
        .with_for_update(of=ClientStock)
        .first()
    )
    if not cs:
        cs = ClientStock(
            product_id=product_id,
            cost_center_id=cost_center_id,
            quantity=0,
        )
        db.add(cs)
        db.flush()
    return cs


def decrement_client_stock(
    cs: ClientStock,
    total: int,
    allow_negative: bool,
) -> None:
    """
    Decrementa o estoque do cliente pelo total vendido.
    Se allow_negative=False, lanÃ§a erro quando nÃ£o houver quantidade suficiente.
    """
    if not allow_negative and cs.quantity < total:
        raise ValueError(
            f"Estoque insuficiente no cliente. Em estoque: {cs.quantity}, vendido: {total}"
        )
    cs.quantity -= total



def business_hours_duration(start_dt: datetime, end_dt: datetime,
                            h_start: int = BUSINESS_START, h_end: int = BUSINESS_END) -> float:
    """
    Retorna quantas horas existem entre start_dt e end_dt considerando apenas
    a janela [h_start:00, h_end:00) de cada dia. Ignora minutos/segundos fora do intervalo.
    """
    if end_dt <= start_dt:
        return 0.0

    total_seconds = 0
    cur = start_dt
    while cur.date() <= end_dt.date():
        day_start = datetime.combine(cur.date(), time(hour=h_start))
        day_end   = datetime.combine(cur.date(), time(hour=h_end))
        # interseÃ§Ã£o com [start_dt, end_dt]
        s = max(day_start, start_dt)
        e = min(day_end,   end_dt)
        if e > s:
            total_seconds += (e - s).total_seconds()
        cur += timedelta(days=1)

    # mÃ­nimo de 60s para evitar divisÃ£o por zero em janelas curtÃ­ssimas
    return max(total_seconds / 3600.0, 1/60)

def get_sales_window_stats_for_product_business_hours(
    db: Session,
    cost_center_id: int,
    product_id: int,
    start_dt: datetime,
    end_dt: datetime,
) -> tuple[int, datetime | None, datetime | None]:
    """
    Soma as vendas (CLIENT_SALE) do produto na loja ENTRE start_dt e end_dt,
    mas apenas dentro do horÃ¡rio comercial (07:00â€“20:00).
    Retorna (total_vendido, first_created_at, last_created_at) dentro do filtro.
    """
    q = (
        db.query(
            func.coalesce(func.sum(StockMovement.quantity), 0),
            func.min(StockMovement.created_at),
            func.max(StockMovement.created_at),
        )
        .filter(
            StockMovement.cost_center_id == cost_center_id,
            StockMovement.product_id == product_id,
            StockMovement.movement_type == MovementType.CLIENT_SALE,
            StockMovement.created_at >= start_dt,
            StockMovement.created_at <= end_dt,
            extract('hour', StockMovement.created_at) >= BUSINESS_START,
            extract('hour', StockMovement.created_at) <  BUSINESS_END,  # atÃ© 19:59:59
        )
    )
    total, first_dt, last_dt = q.first()
    return int(total or 0), first_dt, last_dt

def get_client_stock_qty(db: Session, cost_center_id: int, product_id: int) -> int:
    row = (
        db.query(ClientStock.quantity)
        .filter(ClientStock.cost_center_id == cost_center_id,
                ClientStock.product_id == product_id)
        .first()
    )
    return row[0] if row else 0


def get_sales_quantity(
    db: Session,
    *,
    product_id: int,
    start_date: date,
    end_date: date,
    cost_center_id: int | None = None,
    retail_chain_id: int | None = None,
) -> int:
    """
    Soma a quantidade de vendas (ClientSalesHistory.sold_quantity) para um produto
    no período informado. Permite filtrar por cost_center ou por retail_chain.

    - Se `cost_center_id` for informado, filtra apenas por ele.
    - Caso contrário, se `retail_chain_id` for informado, soma todas as vendas
      dos cost centers associados à cadeia.
    - Se nenhum for informado, soma em todos os cost centers.
    """
    q = (
        db.query(func.coalesce(func.sum(ClientSalesHistory.sold_quantity), 0))
        .filter(
            ClientSalesHistory.product_id == product_id,
            ClientSalesHistory.date >= start_date,
            ClientSalesHistory.date <= end_date,
        )
    )

    if cost_center_id is not None:
        q = q.filter(ClientSalesHistory.cost_center_id == cost_center_id)
    elif retail_chain_id is not None:
        # Junta com CostCenter para filtrar pela retail chain
        q = (
            q.join(CostCenter, CostCenter.id == ClientSalesHistory.cost_center_id)
             .filter(CostCenter.retail_chain_id == retail_chain_id)
        )

    total = q.first()[0]
    return int(total or 0)


def update_client_sales_for_day(
    db: Session,
    *,
    cost_center_id: int,
    product_id: int,
    d: date,
    new_total_sold: int,
) -> int:
    """
    Atualiza a quantidade vendida de um produto em um cost center para um dia específico.
    Ajusta o estoque do cliente pela diferença (delta) e persiste em ClientSalesHistory.

    Regras:
    - new_total_sold >= 0
    - delta = new_total_sold - old_total
      - delta > 0: debita estoque do cliente em 'delta' (não permite negativo)
      - delta < 0: credita estoque do cliente em '-delta'
    - Mantém (se existir) um movimento CLIENT_SALE criado ao meio-dia para o dia (apenas atualiza a quantity);
      não cria novos movimentos para não reprocessar estoque.
    """
    if new_total_sold < 0:
        raise ValueError("total_sold deve ser >= 0")

    # Lock no estoque do cliente
    cs = get_or_create_client_stock_for_update(db, cost_center_id=cost_center_id, product_id=product_id)

    # Vendas existentes no dia
    sales = (
        db.query(ClientSalesHistory)
        .filter_by(cost_center_id=cost_center_id, product_id=product_id, date=d)
        .first()
    )
    old_total = int(sales.sold_quantity) if sales else 0
    delta = int(new_total_sold) - old_total

    # Ajuste de estoque do cliente conforme delta
    if delta > 0:
        # precisa debitar mais estoque
        if cs.quantity < delta:
            raise ValueError(
                f"Estoque insuficiente para aumentar vendas. Em estoque: {cs.quantity}, necessário: {delta}"
            )
        cs.quantity -= delta
    elif delta < 0:
        # devolve para o estoque
        cs.quantity += (-delta)
    # if delta == 0, nada muda no estoque
    db.add(cs)

    # Atualiza histórico diário
    if sales:
        if new_total_sold == 0:
            db.delete(sales)
        else:
            sales.sold_quantity = new_total_sold
            db.add(sales)
    else:
        if new_total_sold > 0:
            sales = ClientSalesHistory(
                product_id=product_id,
                cost_center_id=cost_center_id,
                date=d,
                sold_quantity=new_total_sold,
            )
            db.add(sales)

    # Opcional: atualizar o movimento padrão de meio-dia se existir
    # Apenas sincroniza a quantidade; não cria nem reprocessa estoque
    mv = (
        db.query(StockMovement)
        .filter(
            StockMovement.product_id == product_id,
            StockMovement.cost_center_id == cost_center_id,
            StockMovement.movement_type == MovementType.CLIENT_SALE,
            func.date(StockMovement.created_at) == d,
            extract('hour', StockMovement.created_at) == 12,
        )
        .first()
    )
    if mv:
        mv.quantity = new_total_sold
        db.add(mv)

    db.commit()
    return int(new_total_sold)
