from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas.stock_schemas.stock_movement_schema import  TotalProductStockResponse
from app.models.stockMovement import MovementType
from sqlalchemy import and_ 
from datetime import datetime
from app.models.stockMovement import StockMovement
from app.models.groups import Product


def get_all_stock_movements(db: Session):
    return db.query(StockMovement).offset(0).limit(100).all()


def create_system_in_movement(system_in_data, db) -> StockMovement:
    # TODO : implementar validação
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
            total_in_system=get_current_quantity(product.id, db)
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
