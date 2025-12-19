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
    get_product_entries,
    get_client_loss_history as repo_get_client_loss_history,
    get_client_sales_and_loss_history as repo_get_client_sales_and_loss_history,
    get_daily_sales_and_loss_grouped_by_cost_center as repo_get_daily_sales_and_loss_grouped_by_cost_center,
    get_cycle_analysis_for_cost_center,
)
from app.schemas.stock_schemas.stock_movement_schema import SupplierPurchaseDTO, StockMovementRead
from app.schemas.stock_schemas.stock_movement_schema import (
    StockEntryRead,
    ClientSalesHistoryRead,
    ClientLossHistoryRead,
    ClientSalesLossHistoryRead,
    DailyCostCenterSalesLossGroupRead,
    CycleAnalysisProductRead,
)
from app.schemas.stock_schemas.stock_movement_schema import SupplierPurchaseUpdateDTO, StockEntryReadWithCost, SupplierPurchaseBulkDTO
from datetime import date

from app.service.stock_service.stock_movement_service import StockMovementService


class StockEntryService:
    @staticmethod
    def add_stock_with_cost_average(db: Session, dto:SupplierPurchaseDTO):

        movement = StockMovement(
            product_id=dto.product_id,
            quantity=dto.quantity,
            movement_type=MovementType.SUPPLIER_PURCHASE,
            supplier_id=dto.supplier_id,
            product_unit_cost=dto.unit_cost,
            created_at=datetime.now()
        )

        db.add(movement)
        db.flush()  
        StockMovementService.process_stock_movement(db, movement)

        db.commit()
        return movement

    @staticmethod
    def update_supplier_purchase_entry_service(db: Session, movement_id: int, dto: SupplierPurchaseUpdateDTO) -> StockEntryReadWithCost:
        """
        Edita a última entrada de fornecedor (SUPPLIER_PURCHASE) do produto.
        - Só permite se for a última SUPPLIER_PURCHASE do produto
        - Ajusta o estoque do inventário pelo delta de quantidade
        - Recalcula o custo médio vigente e atualiza o registro atual (ProductCostHistory.end_date IS NULL)
        Retorna a entrada atualizada e o custo médio recalculado.
        """
        dto.ensure_not_empty()

        # Busca movimento
        movement = db.query(StockMovement).filter(StockMovement.id == movement_id).first()
        if not movement:
            raise HTTPException(status_code=404, detail="Movimento não encontrado")
        mt_val = movement.movement_type.value if isinstance(movement.movement_type, MovementType) else movement.movement_type
        if mt_val != MovementType.SUPPLIER_PURCHASE.value:
            raise HTTPException(status_code=400, detail="Somente entradas de fornecedor podem ser editadas")
    
        # Garante que é a última SUPPLIER_PURCHASE deste produto
        newer_count = (
            db.query(StockMovement)
            .filter(
                StockMovement.product_id == movement.product_id,
                StockMovement.movement_type == MovementType.SUPPLIER_PURCHASE.value,
                StockMovement.created_at > movement.created_at,
            )
            .count()
        )
        if newer_count > 0:
            raise HTTPException(status_code=400, detail="Apenas a última entrada de compra pode ser editada")

        # Valores antigos
        old_qty = int(movement.quantity)
        old_unit_cost = float(movement.product_unit_cost) if movement.product_unit_cost is not None else 0.0

        # Novos valores
        new_qty = int(dto.quantity) if dto.quantity is not None else old_qty
        if new_qty <= 0:
            raise HTTPException(status_code=400, detail="quantity deve ser > 0")
        new_unit_cost = float(dto.unit_cost) if dto.unit_cost is not None else old_unit_cost

        # Ajuste de estoque do inventário pelo delta
        stock = db.query(InventoryStock).filter_by(product_id=movement.product_id).with_for_update().first()
        if not stock:
            stock = InventoryStock(product_id=movement.product_id, quantity=0)
            db.add(stock)
            db.flush()
        delta = new_qty - old_qty
        if delta < 0 and stock.quantity < (-delta):
            raise HTTPException(status_code=400, detail="Estoque insuficiente para reduzir a quantidade desta entrada")
        stock.quantity += delta
        db.add(stock)

        # Recalcular custo médio vigente
        # Custo anterior (registro anterior encerrado)
        from app.models.product import ProductCostHistory
        prev_cost_record = (
            db.query(ProductCostHistory)
            .filter(ProductCostHistory.product_id == movement.product_id, ProductCostHistory.end_date.isnot(None))
            .order_by(ProductCostHistory.start_date.desc())
            .first()
        )
        prev_cost = float(prev_cost_record.cost) if prev_cost_record else 0.0

        # Soma de saídas do inventário após esta compra (TO_CLIENT, SUPPLIER_LOSS)
        out_after = (
            db.query(func.coalesce(func.sum(StockMovement.quantity), 0))
            .filter(
                StockMovement.product_id == movement.product_id,
                StockMovement.created_at > movement.created_at,
                StockMovement.movement_type.in_([MovementType.TO_CLIENT.value, MovementType.SUPPLIER_LOSS.value]),
            )
            .scalar()
        )
        out_after = int(out_after or 0)
        # Quantidade no momento anterior à compra
        # current_qty = estoque atual após ajuste do delta
        current_qty = int(stock.quantity)
        q0 = current_qty + out_after - new_qty
        if q0 < 0:
            # Segurança: não deve ocorrer em fluxo consistente; corrige para zero
            q0 = 0

        denom = q0 + new_qty
        if denom <= 0:
            new_avg_cost = new_unit_cost
        else:
            new_avg_cost = ((q0 * prev_cost) + (new_qty * new_unit_cost)) / denom

        # Atualiza o registro de custo vigente (end_date is NULL)
        current_cost_record = (
            db.query(ProductCostHistory)
            .filter_by(product_id=movement.product_id, end_date=None)
            .first()
        )
        if current_cost_record:
            current_cost_record.cost = new_avg_cost
            db.add(current_cost_record)

        # Atualiza o movimento
        movement.quantity = new_qty
        movement.product_unit_cost = new_unit_cost
        if dto.supplier_id is not None:
            movement.supplier_id = dto.supplier_id
        db.add(movement)

        db.commit()
        db.refresh(movement)

        supplier_name = movement.supplier.name if getattr(movement, "supplier", None) else None
        return StockEntryReadWithCost(
            id=movement.id,
            product_id=movement.product_id,
            quantity=movement.quantity,
            unit_cost=float(movement.product_unit_cost) if movement.product_unit_cost is not None else None,
            supplier_id=movement.supplier_id,
            supplier_name=supplier_name,
            created_at=movement.created_at,
            current_avg_cost=float(new_avg_cost) if new_avg_cost is not None else None,
        )


    @staticmethod
    def delete_supplier_purchase_entry_service(db: Session, movement_id: int) -> StockEntryRead:
        """
        Exclui uma entrada de estoque (SUPPLIER_PURCHASE) mais recente para o produto, revertendo:
        - Quantidade do inventário
        - Histórico de custo (reabrindo o registro anterior)

        Restrições:
        - Só permite excluir se for a ÚLTIMA entrada de compra do fornecedor para o produto
        - Não permite se o estoque atual do inventário for menor que a quantidade da entrada
        """
        # Busca movimento
        movement = db.query(StockMovement).filter(StockMovement.id == movement_id).first()
        if not movement:
            raise HTTPException(status_code=404, detail="Movimento não encontrado")

        mt_val = movement.movement_type.value if isinstance(movement.movement_type, MovementType) else movement.movement_type
        if mt_val != MovementType.SUPPLIER_PURCHASE.value:
            raise HTTPException(status_code=400, detail="Somente entradas de fornecedor podem ser excluídas")

        # Verifica se é a última SUPPLIER_PURCHASE para este produto
        newer_count = (
            db.query(StockMovement)
            .filter(
                StockMovement.product_id == movement.product_id,
                StockMovement.movement_type == MovementType.SUPPLIER_PURCHASE.value,
                StockMovement.created_at > movement.created_at,
            )
            .count()
        )
        if newer_count > 0:
            raise HTTPException(status_code=400, detail="Apenas a última entrada de compra pode ser excluída")

        # Verifica estoque do inventário
        stock = db.query(InventoryStock).filter_by(product_id=movement.product_id).with_for_update().first()
        current_qty = stock.quantity if stock else 0
        if current_qty < movement.quantity:
            raise HTTPException(status_code=400, detail="Estoque insuficiente para reverter esta entrada")

        # Ajusta histórico de custo: remove o registro vigente e reabre o anterior
        current_cost_record = (
            db.query(ProductCostHistory)
            .filter_by(product_id=movement.product_id, end_date=None)
            .first()
        )
        if current_cost_record:
            db.delete(current_cost_record)

        previous_cost_record = (
            db.query(ProductCostHistory)
            .filter(ProductCostHistory.product_id == movement.product_id, ProductCostHistory.end_date.isnot(None))
            .order_by(ProductCostHistory.start_date.desc())
            .first()
        )
        if previous_cost_record:
            previous_cost_record.end_date = None
            db.add(previous_cost_record)

        # Reverte estoque do inventário
        if not stock:
            # Deve existir, pois houve entrada, mas garantimos criação para consistência
            stock = InventoryStock(product_id=movement.product_id, quantity=0)
            db.add(stock)
            db.flush()
        stock.quantity = current_qty - movement.quantity
        db.add(stock)

        # Dados de resposta (antes de apagar)
        supplier_name = movement.supplier.name if getattr(movement, "supplier", None) else None
        resp = StockEntryRead(
            id=movement.id,
            product_id=movement.product_id,
            quantity=movement.quantity,
            unit_cost=float(movement.product_unit_cost) if movement.product_unit_cost is not None else None,
            supplier_id=movement.supplier_id,
            supplier_name=supplier_name,
            created_at=movement.created_at,
        )

        # Exclui o movimento
        db.delete(movement)

        db.commit()
        return resp



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
    def add_stock_bulk_with_cost_average(db: Session, bulk: SupplierPurchaseBulkDTO) -> List[StockEntryReadWithCost]:
        if not bulk.items or len(bulk.items) == 0:
            raise HTTPException(status_code=400, detail="Lista de itens vazia")

        results: List[StockEntryReadWithCost] = []
        try:
            for dto in bulk.items:
                movement = StockMovement(
                    product_id=dto.product_id,
                    quantity=dto.quantity,
                    movement_type=MovementType.SUPPLIER_PURCHASE,
                    supplier_id=dto.supplier_id,
                    product_unit_cost=dto.unit_cost,
                    created_at=datetime.now(),
                )
                db.add(movement)
                db.flush()

                # Process inventory and cost
                StockMovementService.process_stock_movement(db, movement)

                # Fetch current average cost after processing
                current_cost_record = (
                    db.query(ProductCostHistory)
                    .filter_by(product_id=movement.product_id, end_date=None)
                    .first()
                )
                current_avg_cost = float(current_cost_record.cost) if current_cost_record else None

                supplier_name = movement.supplier.name if getattr(movement, "supplier", None) else None
                results.append(
                    StockEntryReadWithCost(
                        id=movement.id,
                        product_id=movement.product_id,
                        quantity=movement.quantity,
                        unit_cost=float(movement.product_unit_cost) if movement.product_unit_cost is not None else None,
                        supplier_id=movement.supplier_id,
                        supplier_name=supplier_name,
                        created_at=movement.created_at,
                        current_avg_cost=current_avg_cost,
                    )
                )

            db.commit()
            return results
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Erro ao processar entrada em lote: {str(e)}")

