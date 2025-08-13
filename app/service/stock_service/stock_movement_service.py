from datetime import datetime
from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.product import ProductCostHistory
from app.models.stockMovement import MovementType, StockMovement, InventoryStock
from app.repository.stock.client_stock_repository import get_client_stock_by_cost_center
from app.repository.stock.stock_movement_repository import get_all_stock_movements, get_current_stock
from app.schemas.stock_schemas.stock_movement_schema import SupplierPurchaseDTO

class StockMovementService:
    
    @staticmethod
    def get_current_stock_service(db: Session):
        return get_current_stock(db)

    @staticmethod
    def get_all_movements_service(db: Session):
        
        return get_all_stock_movements(db)

    @staticmethod
    def add_stock_with_cost_average(db: Session, dto:SupplierPurchaseDTO):

        # Criar movimentação
        movement = StockMovement(
            product_id=dto.product_id,
            quantity=dto.quantity,
            movement_type=MovementType.SUPPLIER_PURCHASE.value,
            product_unit_cost=dto.unit_cost, 
            created_at=datetime.now()
        )

        db.add(movement)
        db.flush()  # Garantir ID se precisar usar em seguida

        # Processa movimentação (estoque + custo médio + histórico)
        StockMovementService.process_stock_movement(db, movement)

        db.commit()
        return movement

    @staticmethod
    def process_stock_movement(db: Session, movement: StockMovement):
        """
        Processa qualquer movimento e, se for SUPPLIER_PURCHASE,
        recalcula custo médio e atualiza histórico.
        """
        if movement.movement_type == MovementType.SUPPLIER_PURCHASE.value:
            # Estoque atual
            stock = db.query(InventoryStock).filter_by(product_id=movement.product_id).first()
            if not stock:
                stock = InventoryStock(product_id=movement.product_id, quantity=0)
                db.add(stock)
                db.flush()

            # Buscar custo vigente
            current_cost_record = (
                db.query(ProductCostHistory)
                .filter_by(product_id=movement.product_id, end_date=None)
                .first()
            )
            current_cost = float(current_cost_record.cost) if current_cost_record else 0.0

            # Cálculo custo médio ponderado
            total_qty = stock.quantity + movement.quantity
            if total_qty > 0:
                new_cost = (
                    (stock.quantity * current_cost) +
                    (movement.quantity * float(movement.product_unit_cost))
                ) / total_qty
            else:
                new_cost = float(movement.product_unit_cost)

            # Fecha histórico anterior
            if current_cost_record:
                current_cost_record.end_date = datetime.now()

            # Novo histórico
            new_cost_record = ProductCostHistory(
                product_id=movement.product_id,
                cost=new_cost,
                start_date=datetime.now(),
                end_date=None
            )
            db.add(new_cost_record)

            # Atualiza estoque
            stock.quantity += movement.quantity
            db.add(stock)

        # Aqui você pode tratar outros tipos de movimento


    @staticmethod
    def get_client_stock_service(
        db: Session,
        cost_center_id: int,
        product_ids: Optional[List[int]] = None,
        include_zero: bool = False,
    ) -> List[Dict[str, Any]]:
        return get_client_stock_by_cost_center(
            db=db,
            cost_center_id=cost_center_id,
            product_ids=product_ids,
            include_zero=include_zero,
        )