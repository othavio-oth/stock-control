from collections import defaultdict
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import case, extract, func
from app.models.tickets import Ticket, TicketProduct
from app.schemas.stock_schemas.stock_movement_schema import  StockMovementLost, TotalProductStockResponse
from app.models.stockMovement import MovementType
from sqlalchemy import and_ 
from datetime import datetime
from app.models.stockMovement import StockMovement
from app.models.product import Product


def get_all_stock_movements(db: Session):
    return db.query(StockMovement).offset(0).limit(100).all()


def create_system_in_movement(system_in_data, db) -> StockMovement:
    movement = StockMovement(
        product_id=system_in_data.product_id,
        quantity=system_in_data.quantity,
        movement_type=MovementType.SYSTEM_IN.value,
        supplier=system_in_data.supplier,
        cost_center_id=None
    )
    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement

def get_total_in_system_by_product(db, product_id):
    total_in = db.query(func.sum(StockMovement.quantity)).filter(
        StockMovement.product_id == product_id,
        StockMovement.movement_type == MovementType.SYSTEM_IN
    ).scalar() or 0

    total_out = db.query(func.sum(StockMovement.quantity)).filter(
        StockMovement.product_id == product_id,
        StockMovement.movement_type == MovementType.TO_COST_CENTER
    ).scalar() or 0

    total = total_in - total_out
    return TotalProductStockResponse(product_id=product_id, total_in_system=total)



def get_total_sold_by_cost_center_in_period_grouped_by_product(
    db: Session,
    cost_center_id: int,
    start_date: datetime,
    end_date: datetime,
):
    results = db.query(
        StockMovement.product_id,
        func.sum(StockMovement.quantity).label("total_sold")  # <-- corrigido aqui
    ).filter(
        and_(
            StockMovement.cost_center_id == cost_center_id,
            StockMovement.movement_type == MovementType.OUT,
            StockMovement.created_at >= start_date,
            StockMovement.created_at <= end_date,
        )
    ).group_by(StockMovement.product_id).all()

    return [TotalProductStockResponse(product_id=r.product_id, total_sold=r.total_sold) for r in results]


def get_current_quantity(product_id: int, db: Session):
    total_in = db.query(func.sum(StockMovement.quantity)).filter(
        StockMovement.product_id == product_id,
        StockMovement.movement_type == MovementType.SYSTEM_IN
    ).scalar() or 0

    total_out = db.query(func.sum(StockMovement.quantity)).filter(
        StockMovement.product_id == product_id,
        StockMovement.movement_type == MovementType.TO_COST_CENTER
    ).scalar() or 0

    return total_in - total_out

def get_all_product_quantities_in_system(db: Session):

    products = db.query(Product).filter(Product.status == True).all()

    result = [
        TotalProductStockResponse(
            product_id=product.id,
            total=get_current_quantity(product.id, db)
        )
        for product in products
    ]

    return result

    
def move_stock_to_cost_center(movement_data, db) -> StockMovement:

    movement = StockMovement(
        product_id=movement_data.product_id,
        quantity=movement_data.quantity,
        movement_type=MovementType.TO_COST_CENTER.value,
        cost_center_id=movement_data.cost_center_id
    )

    db.add(movement)
    db.commit()
    db.refresh(movement)

    return movement


def get_current_quantity_by_cost_center(
    db: Session,
    product_id: int,
    cost_center_id: int
) -> int:
    total_in = db.query(func.sum(StockMovement.quantity)).filter(
        StockMovement.product_id == product_id,
        StockMovement.cost_center_id == cost_center_id,
        StockMovement.movement_type == MovementType.TO_COST_CENTER
    ).scalar() or 0

    total_out = db.query(func.sum(StockMovement.quantity)).filter(
        StockMovement.product_id == product_id,
        StockMovement.cost_center_id == cost_center_id,
        StockMovement.movement_type == MovementType.RETURN_TO_SYSTEM
    ).scalar() or 0

    return total_in - total_out


def get_all_product_quantities_in_cost_center(db: Session, cost_center_id: int) -> List[TotalProductStockResponse]:
    products = db.query(Product).filter(Product.status == True).all()
    
    result = []
    for product in products:
        quantity = get_current_quantity_by_cost_center(db, product.id, cost_center_id)
        result.append(
            TotalProductStockResponse(product_id=product.id, total_in_system=quantity)
        )
    
    return result

def create_stock_movements_for_sales(ticket_products: list[TicketProduct],center_id: int, db: Session):
    for tp in ticket_products:
        stock_movement = StockMovement(
            product_id=tp.product_id,
            quantity=tp.quantity_sold,
            movement_type=MovementType.SOLD,
            cost_center_id=center_id
        )
        db.add(stock_movement)
    
    db.commit()
    
    
def get_cost_center_stock(cost_center_id: int, db: Session):


    stock = (
        db.query(
            StockMovement.product_id,
            func.sum(
                case(
                    (StockMovement.movement_type.in_([MovementType.SYSTEM_IN, MovementType.TO_COST_CENTER]), StockMovement.quantity),
                    (StockMovement.movement_type.in_([MovementType.SOLD, MovementType.LOST]), -StockMovement.quantity),
                    else_=0
                )
            ).label("total")
        )
        .join(Product, Product.id == StockMovement.product_id)
        .filter(StockMovement.cost_center_id == cost_center_id)
        .group_by(StockMovement.product_id, Product.description)
        .having(func.sum(
            case(
                (StockMovement.movement_type.in_([MovementType.SYSTEM_IN, MovementType.TO_COST_CENTER]), StockMovement.quantity),
                (StockMovement.movement_type.in_([MovementType.SOLD, MovementType.LOST]), -StockMovement.quantity),
                else_=0
            )
        ) > 0)
        .all()
    )


    return stock

def get_monthly_sales_losses_stats(db: Session, year: int = None) -> List[Dict[str, Any]]:
    """
    Controller para estatísticas mensais de vendas e perdas
    """
    if year is None:
        year = datetime.now().year
    
    month_map = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }
    
    # Query para vendas
    sales = db.query(
        extract('month', Ticket.order_date).label('month'),
        func.sum(TicketProduct.quantity_sold).label('sales')
    ).join(Ticket).filter(
        and_(
            TicketProduct.quantity_sold > 0,
            extract('year', Ticket.order_date) == year
        )
    ).group_by(extract('month', Ticket.order_date)).all()
    
    # Query para perdas
    losses = db.query(
        extract('month', StockMovement.created_at).label('month'),
        func.sum(StockMovement.quantity).label('losses')
    ).filter(
        and_(
            StockMovement.movement_type == MovementType.LOST,
            extract('year', StockMovement.created_at) == year
        )
    ).group_by(extract('month', StockMovement.created_at)).all()
    
    # Consolidar resultados
    stats = {month: {"month": name, "sales": 0, "losses": 0} 
            for month, name in month_map.items()}
    
    for month, amount in sales:
        stats[month]["sales"] = amount or 0
        
    for month, amount in losses:
        stats[month]["losses"] = amount or 0
    
    return list(stats.values())



def register_stock_loss(
    db: Session, 
    loss_data: StockMovementLost
) -> StockMovement:


    # Validação adicional
    if loss_data.quantity <= 0:
        raise ValueError("A quantidade deve ser maior que zero")
    
    try:
        # Cria o movimento de perda
        loss_movement = StockMovement(
            **loss_data.model_dump(exclude_unset=True),
            created_at=loss_data.created_at or datetime.now()
        )
        
        db.add(loss_movement)
        db.commit()
        db.refresh(loss_movement)
        
        return loss_movement
        
    except Exception as e:
        db.rollback()
        raise ValueError(f"Falha ao registrar perda: {str(e)}")