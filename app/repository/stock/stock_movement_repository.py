from collections import defaultdict
from typing import Any, Dict, List, Optional, Set
from sqlalchemy.orm import Session
from sqlalchemy import case, extract, func
from app.models.tickets import Ticket, TicketProduct
from app.schemas.stock_schemas.stock_movement_schema import  StockMovementLost, TotalProductStockResponse
from app.models.stockMovement import ClientLossHistory, ClientSalesHistory, ClientStock, MovementType, InventoryStock
from sqlalchemy import and_ 
from datetime import datetime
from app.models.stockMovement import StockMovement
from app.models.product import Product

from sqlalchemy.orm import Session
from datetime import date

def process_stock_movement(db: Session, movement: StockMovement):
    """
    Atualiza estoques do INVENTÁRIO e/ou do CLIENTE conforme o tipo de movimento.
    Regras:
      - SUPPLIER_PURCHASE: inventário ++ (exige supplier_id)
      - SUPPLIER_LOSS: inventário --
      - TO_CLIENT: inventário -- e cliente ++
      - CLIENT_SALE: cliente -- (+ histórico de venda)
      - CLIENT_LOSS: cliente -- (+ histórico de perda)
    """
    # -------- INVENTÁRIO (fornecedor) --------
    if movement.movement_type in [
        MovementType.SUPPLIER_PURCHASE,
        MovementType.SUPPLIER_LOSS,
        MovementType.TO_CLIENT,
    ]:
        if movement.movement_type == MovementType.SUPPLIER_PURCHASE and not movement.supplier_id:
            raise ValueError("Movimentações SUPPLIER_PURCHASE exigem supplier_id.")

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
            # SUPPLIER_LOSS ou TO_CLIENT → debita inventário
            if supplier_stock.quantity < movement.quantity:
                raise ValueError(
                    f"Estoque do inventário insuficiente: "
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

            # Histórico de vendas (por dia)
            sales_record = (
                db.query(ClientSalesHistory)
                  .filter_by(product_id=movement.product_id,
                             cost_center_id=movement.cost_center_id,
                             date=date.today())
                  .first()
            )
            if not sales_record:
                sales_record = ClientSalesHistory(
                    product_id=movement.product_id,
                    cost_center_id=movement.cost_center_id,
                    date=date.today(),
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

            # Histórico de perdas (por dia)
            loss_record = (
                db.query(ClientLossHistory)
                  .filter_by(product_id=movement.product_id,
                             cost_center_id=movement.cost_center_id,
                             date=date.today())
                  .first()
            )
            if not loss_record:
                loss_record = ClientLossHistory(
                    product_id=movement.product_id,
                    cost_center_id=movement.cost_center_id,
                    date=date.today(),
                    lost_quantity=0,
                    reason="Perda registrada"
                )
                db.add(loss_record)
            loss_record.lost_quantity += movement.quantity

    db.commit()

def get_all_stock_movements(db: Session):
    return db.query(StockMovement).offset(0).limit(100).all()


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
    Retorna os dias que já possuem vendas registradas no intervalo [start, end].
    Útil para evitar duplicidade ao distribuir o total por dia.
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
    Faz upsert da venda diária (somando ao que já existir no dia).
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


# ——— StockMovement ————————————————————————————————————————————————

def create_client_sale_movement(
    db: Session,
    product_id: int,
    cost_center_id: int,
    qty: int,
    created_at: datetime,
    product_unit_cost: Optional[float] = None,
) -> None:
    """
    Cria uma movimentação do tipo CLIENT_SALE no dia da venda.
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


# ——— ClientStock ————————————————————————————————————————————————

def get_or_create_client_stock_for_update(
    db: Session,
    cost_center_id: int,
    product_id: int,
) -> ClientStock:
    """
    Retorna o ClientStock com lock (FOR UPDATE). Cria com quantity=0 se não existir.
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
    Se allow_negative=False, lança erro quando não houver quantidade suficiente.
    """
    if not allow_negative and cs.quantity < total:
        raise ValueError(
            f"Estoque insuficiente no cliente. Em estoque: {cs.quantity}, vendido: {total}"
        )
    cs.quantity -= total
