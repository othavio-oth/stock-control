from datetime import datetime
from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.product import ProductCostHistory
from app.models.stockMovement import MovementType, StockMovement, InventoryStock
from app.repository.stock.client_stock_repository import get_client_stock_by_cost_center
from app.repository.stock.stock_movement_repository import get_all_stock_movements, get_current_stock, get_product_entries
from app.schemas.stock_schemas.stock_movement_schema import SupplierPurchaseDTO, StockMovementLost, RegisterClientSalesDTO, StockMovementRead
from app.schemas.stock_schemas.stock_movement_schema import StockEntryRead

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
    def add_stock_with_cost_average(db: Session, dto:SupplierPurchaseDTO):

        # Criar movimentaÃ§Ã£o
        movement = StockMovement(
            product_id=dto.product_id,
            quantity=dto.quantity,
            movement_type=MovementType.SUPPLIER_PURCHASE.value,
            supplier_id=dto.supplier_id,
            product_unit_cost=dto.unit_cost,
            created_at=datetime.now()
        )

        db.add(movement)
        db.flush()  # Garantir ID se precisar usar em seguida

        # Processa movimentaÃ§Ã£o (estoque + custo mÃ©dio + histÃ³rico)
        StockMovementService.process_stock_movement(db, movement)

        db.commit()
        return movement

    @staticmethod
    def process_stock_movement(db: Session, movement: StockMovement):
        """
        Processa qualquer movimento e, se for SUPPLIER_PURCHASE,
        recalcula custo mÃ©dio e atualiza histÃ³rico.
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

            # Novo histÃ³rico
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

        # Aqui vocÃª pode tratar outros tipos de movimento
        else:
            # Delegar ao repositório para atualizar estoques/históricos
            from app.repository.stock.stock_movement_repository import process_stock_movement as _repo_process
            _repo_process(db, movement)


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
    def get_product_entries_service(db: Session, product_id: int, page: int = 1, page_size: int = 20):
        total, items = get_product_entries(db, product_id=product_id, page=page, page_size=page_size)
        # map to schema payload
        result = []
        for mv in items:
            result.append(
                StockEntryRead(
                    id=mv.id,
                    product_id=mv.product_id,
                    quantity=mv.quantity,
                    unit_cost=float(mv.product_unit_cost) if mv.product_unit_cost is not None else None,
                    supplier_id=mv.supplier_id,
                    supplier_name=(mv.supplier.name if getattr(mv, "supplier", None) else None),
                    created_at=mv.created_at,
                )
            )
        return result

    @staticmethod
    def register_stock_loss_service(db: Session, loss_data: StockMovementLost):
        if not loss_data.cost_center_id:
            raise HTTPException(status_code=400, detail="cost_center_id é obrigatório para perdas do cliente")
        if loss_data.quantity <= 0:
            raise HTTPException(status_code=400, detail="quantity deve ser > 0")

        movement = StockMovement(
            product_id=loss_data.product_id,
            quantity=loss_data.quantity,
            movement_type=MovementType.CLIENT_LOSS,
            cost_center_id=loss_data.cost_center_id,
            created_at=loss_data.created_at or datetime.now(),
        )
        db.add(movement)
        db.flush()

        from app.repository.stock.stock_movement_repository import process_stock_movement as _repo_process
        _repo_process(db, movement)

        db.commit()
        db.refresh(movement)
        return movement

    @staticmethod
    def register_client_sale_service(db: Session, dto: RegisterClientSalesDTO) -> StockMovement:
        if dto.total_sold <= 0:
            raise HTTPException(status_code=400, detail="total_sold deve ser > 0")
        # Lock e validação de estoque do cliente
        from app.repository.stock.stock_movement_repository import (
            get_or_create_client_stock_for_update,
            decrement_client_stock,
            upsert_sales_for_day,
        )
        cs = get_or_create_client_stock_for_update(
            db=db,
            cost_center_id=dto.cost_center_id,
            product_id=dto.product_id,
        )
        decrement_client_stock(cs, total=dto.total_sold, allow_negative=False)
        # Atualiza histórico diário de vendas para a data informada
        upsert_sales_for_day(
            db=db,
            cost_center_id=dto.cost_center_id,
            product_id=dto.product_id,
            d=dto.registration_date,
            qty=dto.total_sold,
        )

        # Registra um movimento para fins de auditoria
        mv = StockMovement(
            product_id=dto.product_id,
            quantity=dto.total_sold,
            movement_type=MovementType.CLIENT_SALE,
            cost_center_id=dto.cost_center_id,
            created_at=datetime.combine(dto.registration_date, datetime.min.time()).replace(hour=12, minute=0, second=0),
        )
        db.add(mv)

        db.commit()
        db.refresh(mv)
        return mv
