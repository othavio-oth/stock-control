from datetime import date
from typing import  Optional

from fastapi import HTTPException
from app.models.stockMovement import (
    InventoryVisit,
    InventoryVisitProduct,

)

from . import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, or_, and_


def get_all_tickets(page:int,db: Session):
    page_size = 20
    offset = (page - 1) * page_size
    total = db.query(Ticket).count()
    tickets = (
        db.query(Ticket)
        .options(
            joinedload(Ticket.products).joinedload(TicketProduct.product),
            joinedload(Ticket.inventory_visits)
            .joinedload(InventoryVisit.products)
            .joinedload(InventoryVisitProduct.product),
            joinedload(Ticket.inventory_visits).joinedload(InventoryVisit.cost_center),
        )
        .offset(offset)
        .limit(page_size)
        .all()
    )
    total_pages = (total + page_size - 1) // page_size
    return {
    "items": tickets,
    "total": total,
    "page": page,
    "page_size": page_size,
    "total_pages": total_pages
    }

def get_ticket_by_id(db: Session, ticket_id: int):
    return (
        db.query(Ticket)
        .options(
            joinedload(Ticket.products).joinedload(TicketProduct.product),
            joinedload(Ticket.inventory_visits)
            .joinedload(InventoryVisit.products)
            .joinedload(InventoryVisitProduct.product),
            joinedload(Ticket.inventory_visits).joinedload(InventoryVisit.cost_center),
        )
        .filter(Ticket.id == ticket_id)
        .first()
    )

# tickets_repository.py
from sqlalchemy.orm import Session, joinedload
from app.models.tickets import Ticket, TicketProduct

def _to_dict(obj, **kwargs):
    # v2
    if hasattr(obj, "model_dump"):
        return obj.model_dump(**kwargs)
    # v1
    if hasattr(obj, "dict"):
        return obj.dict(**kwargs)
    # já é dict
    return obj

def create_ticket(db: Session, ticket_data):
    # 1) se vierem produtos no payload
    items = getattr(ticket_data, "products", []) or []

    # 2) remover "products" antes de instanciar Ticket
    data = _to_dict(ticket_data, exclude={"products"})
    ticket = Ticket(**data)  # <-- sem .dict()
    db.add(ticket)
    db.flush()  # garante ticket.id

    # 3) criar TicketProduct para cada item
    for it in items:
        itd = _to_dict(it)
        tp = TicketProduct(
            ticket_id=ticket.id,
            product_id=itd["product_id"],
            sent_quantity=itd.get("sent_quantity", itd.get("quantity_ordered")),  # alias resolved in schema
            unit_price=itd.get("unit_price"),
            entry_price=itd.get("entry_price"),
        )
        db.add(tp)

    db.commit()

    # 4) retornar já com relacionamentos carregados
    ticket = (
        db.query(Ticket)
          .options(joinedload(Ticket.products).joinedload(TicketProduct.product))
          .get(ticket.id)
    )
    return ticket



def update_ticket(db, ticket_id, ticket_data):
    """
    Atualiza campos do Ticket e, se enviados, substitui a lista de products.
    - Ignora "id" do payload para o próprio Ticket.
    - Se "products" vier no payload, trata como estado desejado completo:
      faz upsert dos informados e remove os ausentes.
    """
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        return None

    raw = _to_dict(ticket_data)
    products = raw.pop("products", None)
    raw.pop("id", None)

    # Atualiza campos simples do Ticket
    for key, value in raw.items():
        if hasattr(ticket, key):
            setattr(ticket, key, value)

    # Substituição/Upsert dos produtos (se enviados)
    if products is not None:
        desired_ids = set()
        for it in products or []:
            item = _to_dict(it)
            product_id = item.get("product_id")
            if not product_id:
                continue
            desired_ids.add(product_id)
            tp = (
                db.query(TicketProduct)
                .filter(TicketProduct.ticket_id == ticket_id, TicketProduct.product_id == product_id)
                .first()
            )
            if tp:
                for field in ("sent_quantity", "unit_price", "entry_price"):
                    if field in item and item[field] is not None:
                        setattr(tp, field, item[field])
            else:
                db.add(
                    TicketProduct(
                        ticket_id=ticket_id,
                        product_id=product_id,
                        sent_quantity=item.get("sent_quantity", item.get("quantity_ordered", 0)),
                        unit_price=item.get("unit_price"),
                        entry_price=item.get("entry_price"),
                    )
                )
        # Remove os que não estão no payload
        existing = db.query(TicketProduct).filter(TicketProduct.ticket_id == ticket_id).all()
        for tp in existing:
            if tp.product_id not in desired_ids:
                db.delete(tp)

    try:
        db.commit()
        db.refresh(ticket)
    except IntegrityError as e:
        db.rollback()
        # nomes duplicados ou outras violações de unicidade
        raise HTTPException(status_code=400, detail="Não foi possível atualizar o ticket: conflito de dados (nome duplicado ou similar)")
    return ticket

def delete_ticket(db, ticket_id):
    ticket = get_ticket_by_id(db, ticket_id)
    if ticket:
        db.delete(ticket)
        db.commit()
    return None

def get_products_by_ticket(db, ticket_id):
    return db.query(TicketProduct).filter(TicketProduct.ticket_id == ticket_id).order_by(TicketProduct.id).all()








def get_last_approved_ticket_id_for_cc_product(
    db: Session, cost_center_id: int, product_id: Optional[int]
) -> Optional[int]:
    """
    Retorna o ID do último ticket aprovado considerando APENAS "approved_at".
    - Se "product_id" for fornecido: filtra por (cost_center_id, product_id).
    - Se "product_id" não for fornecido (None/0): considera apenas o cost_center.

    Importante: não usa "order_date" como fallback. Se não houver tickets com
    "approved_at" preenchido, retorna None.
    """
    if product_id:
        q = (
            db.query(Ticket.id)
            .join(TicketProduct, TicketProduct.ticket_id == Ticket.id)
            .filter(
                Ticket.cost_center_id == cost_center_id,
                TicketProduct.product_id == product_id,
                Ticket.approved_at.isnot(None),
            )
            .order_by(desc(Ticket.approved_at), desc(Ticket.id))
            .limit(1)
        ).first()
        return q[0] if q else None
    else:
        q = (
            db.query(Ticket.id)
            .filter(
                Ticket.cost_center_id == cost_center_id,
                Ticket.approved_at.isnot(None),
            )
            .order_by(desc(Ticket.approved_at), desc(Ticket.id))
            .limit(1)
        ).first()
        return q[0] if q else None











def get_last_approved_ticket_by_cost_center(db: Session, cost_center_id: int):
    return (
        db.query(Ticket)
        .filter(Ticket.cost_center_id == cost_center_id, Ticket.status == "approved")
        .order_by(desc(Ticket.order_date), desc(Ticket.id))
        .first()
    )


def get_previous_approved_ticket_for_cost_center(
    db: Session,
    *,
    cost_center_id: int,
    current_ticket_id: int,
) -> Optional[Ticket]:
    current_ticket = (
        db.query(Ticket)
        .filter(Ticket.id == current_ticket_id, Ticket.cost_center_id == cost_center_id)
        .first()
    )
    if not current_ticket:
        return None

    current_approved_at = current_ticket.approved_at
    query = (
        db.query(Ticket)
        .filter(
            Ticket.cost_center_id == cost_center_id,
            Ticket.approved_at.isnot(None),
        )
    )

    if current_approved_at:
        query = query.filter(
            or_(
                Ticket.approved_at < current_approved_at,
                and_(
                    Ticket.approved_at == current_approved_at,
                    Ticket.id < current_ticket_id,
                ),
            )
        )
    else:
        query = query.filter(Ticket.id < current_ticket_id)

    return (
        query.order_by(desc(Ticket.approved_at), desc(Ticket.id))
        .limit(1)
        .first()
    )
def set_ticket_status(db: Session, ticket_id: int, status: str):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        return None
    ticket.status = status
    db.commit()
    db.refresh(ticket)
    return ticket

def create_next_cycle_ticket(db: Session, base_ticket: Ticket, name: str | None = None, description: str | None = None):
    new_ticket = Ticket(
        name=name or f"Ticket {base_ticket.cost_center_id}-{date.today().isoformat()}",
        description=description,
        status="open",
        cost_center_id=base_ticket.cost_center_id,
        order_date=date.today(),
        created_by=base_ticket.created_by,
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket




