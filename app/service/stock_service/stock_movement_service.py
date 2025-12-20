from datetime import datetime
from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.product import ProductCostHistory
from app.models.stockMovement import MovementType, StockMovement, InventoryStock, ClientSalesHistory
from app.repository.stock.client_stock_repository import get_client_stock_by_cost_center, update_client_stock_quantity
from app.repository.stock.stock_movement_repository import (
    get_all_stock_movements,
    get_current_stock,
    get_client_loss_history as repo_get_client_loss_history,
    get_client_sales_and_loss_history as repo_get_client_sales_and_loss_history,
    get_daily_sales_and_loss_grouped_by_cost_center as repo_get_daily_sales_and_loss_grouped_by_cost_center,
    get_cycle_analysis_for_cost_center,
)
from app.schemas.stock_schemas.stock_movement_schema import SupplierPurchaseDTO, StockMovementRead
from app.schemas.stock_schemas.stock_movement_schema import (
    ClientSalesHistoryRead,
    ClientLossHistoryRead,
    ClientSalesLossHistoryRead,
    DailyCostCenterSalesLossGroupRead,
    CycleAnalysisProductRead,
)

from datetime import date

class StockMovementService:
    
    @staticmethod
    def get_current_stock_service(db: Session):
        return get_current_stock(db)

    @staticmethod
    def get_all_movements_service(
        db: Session,
        movement_type: Optional[str] = None,
        product_id: Optional[int] = None,
    ):
        return get_all_stock_movements(db, movement_type=movement_type, product_id=product_id)

  
    @staticmethod
    def process_stock_movement(db: Session, movement: StockMovement):
        """
        Processa qualquer movimento e, se for SUPPLIER_PURCHASE,
        recalcula custo mÃ©dio e atualiza histÃ³rico.
        """
        mt_val = movement.movement_type.value if isinstance(movement.movement_type, MovementType) else movement.movement_type
        if mt_val == MovementType.SUPPLIER_PURCHASE.value:
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

            # CÃ¡lculo custo mÃ©dio ponderado
            total_qty = stock.quantity + movement.quantity
            if total_qty > 0:
                new_cost = (
                    (stock.quantity * current_cost) +
                    (movement.quantity * float(movement.product_unit_cost))
                ) / total_qty
            else:
                new_cost = float(movement.product_unit_cost)

            # Fecha histÃ³rico anterior
            if current_cost_record:
                current_cost_record.end_date = datetime.now()

            new_cost_record = ProductCostHistory(
                product_id=movement.product_id,
                cost=new_cost,
                start_date=datetime.now(),
                end_date=None
            )
            db.add(new_cost_record)

            stock.quantity += movement.quantity
            db.add(stock)

        else:
            # Delegar ao repositório para atualizar estoques/históricos
            from app.repository.stock.stock_movement_repository import process_stock_movement as _repo_process
            _repo_process(db, movement)


    @staticmethod
    def reset_inventory_stock_service(db: Session) -> int:
        try:
            updated_rows = db.query(InventoryStock).update({InventoryStock.quantity: 0}, synchronize_session=False)
            db.commit()
            return int(updated_rows or 0)
        except Exception as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao zerar estoque do inventario: {exc}")

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
        
    @staticmethod
    def update_client_stock_quantity_service(
        db: Session,
        cost_center_id: int,
        product_id: int,
        quantity: int,
        upsert: bool = True,
    ) -> dict:
        return update_client_stock_quantity(
            db=db,
            cost_center_id=cost_center_id,
            product_id=product_id,
            quantity=quantity,
            upsert=upsert,
        )

    @staticmethod
    def get_client_sales_history_service(
        db: Session,
        cost_center_id: int,
        product_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[ClientSalesHistoryRead]:
        q = db.query(ClientSalesHistory).filter(ClientSalesHistory.cost_center_id == cost_center_id)
        if product_id is not None:
            q = q.filter(ClientSalesHistory.product_id == product_id)
        if start_date is not None:
            q = q.filter(ClientSalesHistory.date >= start_date)
        if end_date is not None:
            q = q.filter(ClientSalesHistory.date <= end_date)
        q = q.order_by(ClientSalesHistory.date.desc())
        items = q.all()
        return [ClientSalesHistoryRead.model_validate(i) for i in items]

    @staticmethod
    def get_client_loss_history_service(
        db: Session,
        *,
        cost_center_id: int,
        product_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[ClientLossHistoryRead]:
        items = repo_get_client_loss_history(
            db,
            cost_center_id=cost_center_id,
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
        )
        if not items and product_id is not None:
            target_date = end_date or start_date or date.today()
            return [
                ClientLossHistoryRead(
                    id=0,
                    cost_center_id=cost_center_id,
                    product_id=product_id,
                    date=target_date,
                    lost_quantity=0,
                    reason=None,
                    observed_at=None,
                )
            ]
        return [ClientLossHistoryRead.model_validate(i) for i in items]

    @staticmethod
    def get_client_sales_and_loss_history_service(
        db: Session,
        cost_center_id: int,
        product_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[ClientSalesLossHistoryRead]:
        items = repo_get_client_sales_and_loss_history(
            db,
            cost_center_id=cost_center_id,
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
        )
        return [ClientSalesLossHistoryRead.model_validate(i) for i in items]

    @staticmethod
    def get_daily_sales_and_loss_by_cost_center_service(
        db: Session,
        *,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        cost_center_ids: Optional[List[int]] = None,
        product_id: Optional[int] = None,
    ) -> list[DailyCostCenterSalesLossGroupRead]:
        items = repo_get_daily_sales_and_loss_grouped_by_cost_center(
            db,
            start_date=start_date,
            end_date=end_date,
            cost_center_ids=cost_center_ids,
            product_id=product_id,
        )
        return [DailyCostCenterSalesLossGroupRead.model_validate(i) for i in items]

    @staticmethod
    def get_cycle_analysis_service(
        db: Session,
        *,
        ticket_id: int,
        max_cycles: int,
    ) -> list[CycleAnalysisProductRead]:
        items = get_cycle_analysis_for_cost_center(
            db,
            ticket_id=ticket_id,
            max_cycles=max_cycles,
        )
        return [CycleAnalysisProductRead.model_validate(i) for i in items]

    @staticmethod
    def get_sales_quantity_service(
        db: Session,
        *,
        product_id: int,
        start_date: date,
        end_date: date,
        cost_center_id: Optional[int] = None,
        retail_chain_id: Optional[int] = None,
    ) -> int:
        from app.repository.stock.stock_movement_repository import get_sales_quantity
        return get_sales_quantity(
            db,
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
            cost_center_id=cost_center_id,
            retail_chain_id=retail_chain_id,
        )

    @staticmethod
    def update_client_sale_for_day_service(
        db: Session,
        *,
        cost_center_id: int,
        product_id: int,
        d: date,
        new_total_sold: int,
    ) -> int:
        from app.repository.stock.stock_movement_repository import update_client_sales_for_day
        return update_client_sales_for_day(
            db,
            cost_center_id=cost_center_id,
            product_id=product_id,
            d=d,
            new_total_sold=new_total_sold,
        )
