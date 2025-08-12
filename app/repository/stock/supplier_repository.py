from pytest import Session

from app.models.stockMovement import InventoryStock, MovementType, StockMovement



def update_supplier_stock(db: Session, movement: StockMovement):
    supplier_stock = db.query(InventoryStock).filter_by(product_id=movement.product_id).first()

    if not supplier_stock:
        supplier_stock = InventoryStock(product_id=movement.product_id, quantity=0)
        db.add(supplier_stock)

    if movement.movement_type == MovementType.SUPPLIER_PURCHASE.value:
        supplier_stock.quantity += movement.quantity
    elif movement.movement_type == MovementType.SUPPLIER_LOSS.value:
        supplier_stock.quantity -= movement.quantity
    elif movement.movement_type == MovementType.TO_CLIENT.value:
        supplier_stock.quantity -= movement.quantity

    db.commit()
