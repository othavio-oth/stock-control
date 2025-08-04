from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, Optional
from fastapi import HTTPException
from sqlalchemy import and_, func, or_

from app.models.stockMovement import MovementType, StockMovement
from app.models.tickets import CostCenter, Ticket, TicketProduct
from . import *

def get_all_products_no_pagination(db):
    products = db.query(Product).filter(Product.is_active == True).order_by(Product.id).all()
    return products
    
def get_all_active_products(page,db):
    page_size = 20
    offset = (page - 1) * page_size
    query = db.query(Product).filter(Product.is_active == True)
    total = query.count()
    products = query.order_by(Product.id).offset(offset).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": products,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }
    


def get_system_in_movements_by_product(product_id: int, page: int, db: Session) -> Dict[str, Any]:
    """
    Retorna o histórico de entradas de um produto com paginação
    (registros mais recentes primeiro)
    """
    page_size = 20
    offset = (page - 1) * page_size
    
    # Query base com ordenação por data decrescente
    query = db.query(StockMovement).filter(
        StockMovement.movement_type == MovementType.SYSTEM_IN.value,
        StockMovement.product_id == product_id
    ).order_by(StockMovement.created_at.desc())
    
    total = query.count()
    movements = query.offset(offset).limit(page_size).all()
    
    # Obter informações do produto
    product = db.query(Product).filter(Product.id == product_id).first()
    
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": movements,
        "product": {
            "id": product.id,
            "description": product.description,
            "custom_id": product.custom_id
        },
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

def get_product_by_id(product_id, db):
    return db.query(Product).filter(Product.id == product_id, Product.is_active==True).first()

def create_product(db, product_data):
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db, product_id, product_data):
    product = get_product_by_id(product_id, db)
    if product:
        for key, value in product_data.dict().items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
    return product



def delete_product( db: Session, product: Product):
    
    product.is_active = False
    product.deleted_at = datetime.now()  # Opcional
    db.commit()
    return {"message": "Produto desativado com sucesso."}


def search_products_by_term( search_term: str,page:int,db: Session):
    page_size = 20
    offset = (page - 1) * page_size
    base_query = db.query(Product).filter(
            or_(
                Product.custom_id == int(search_term) if search_term.isdigit() else False,
                Product.description.ilike(f"%{search_term}%"),
            )
        )
    total = base_query.count()
    total_pages = (total + page_size - 1) // page_size

    tickets = base_query.offset(offset).limit(page_size).all()
    return {
    "items": tickets,
    "total": total,
    "page": page,
    "page_size": page_size,
    "total_pages": total_pages
    }
    


# def get_product_sales( db: Session, product_id: int, cost_center_id: int, period_days: int = 30):
#        # 1. Período de análise
#         end_date = datetime.now()
#         start_date = end_date - timedelta(days=period_days)
        
#         # 2. Busca dados de vendas
#         sales = db.query(
#             func.sum(TicketProduct.quantity_ordered).label("total_sold"),
#             func.sum(TicketProduct.unit_price * TicketProduct.quantity_ordered).label("total_revenue")
#         ).join(Ticket).filter(
#             and_(
#                 TicketProduct.product_id == product_id,
#                 Ticket.cost_center_id == cost_center_id,
#                 Ticket.status == "closed",
#                 Ticket.closed_at.between(start_date, end_date)
#         )).first()

#         # 3. Busca dados de estoque
#         stock = db.query(
#             func.sum(StockMovement.quantity).label("total_stock")
#         ).filter(
#             and_(
#                 StockMovement.product_id == product_id,
#                 StockMovement.cost_center_id == cost_center_id,
#                 StockMovement.movement_type == "SYSTEM_IN",
#                 StockMovement.created_at <= end_date)
#         ).scalar() or 0

#         # 4. Busca preço de custo
#         product = db.query(Product).get(product_id)
#         cost_center = db.query(CostCenter).get(cost_center_id)

#         # 5. Cálculos
#         total_sold = sales.total_sold or 0
#         total_revenue = sales.total_revenue or Decimal('0')
#         total_stock = Decimal(stock)
        
#         # 6. Métricas calculadas
#         return {
#             "product_id": product_id,
#             "product_name": product.description,
#             "cost_center_id": cost_center_id,
#             "cost_center_name": cost_center.name,
#             "period_days": period_days,
#             "total_sold": total_sold,
#             "total_revenue": total_revenue,
#             "avg_sale_price": total_revenue / total_sold if total_sold > 0 else Decimal('0'),
#             "stock_utilization": float((Decimal(total_sold) / total_stock * 100)) if total_stock > 0 else 0.0,
#             "total_profit": total_revenue - (product.cost_inside * total_sold),
#             "profit_margin": float(((total_revenue - (product.cost_inside * total_sold)) / total_revenue * 100)) if total_revenue > 0 else 0.0,
#             "total_losses": max(total_stock - total_sold, 0),
#             "loss_percentage": float(((total_stock - total_sold) / total_stock * 100)) if total_stock > 0 else 0.0
#         }