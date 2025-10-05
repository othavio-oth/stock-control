from datetime import datetime
from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.product import ProductCostHistory
from app.models.stockMovement import MovementType, StockMovement, InventoryStock, ClientSalesHistory, ClientLossHistory
from app.repository.stock.client_stock_repository import get_client_stock_by_cost_center, update_client_stock_quantity
from app.repository.stock.stock_movement_repository import get_all_stock_movements, get_current_stock, get_product_entries
from app.schemas.stock_schemas.stock_movement_schema import SupplierPurchaseDTO, StockMovementLost, RegisterClientSalesDTO, StockMovementRead
from app.schemas.stock_schemas.stock_movement_schema import StockEntryRead, ClientSalesHistoryRead, ClientLossHistoryRead
from app.schemas.stock_schemas.stock_movement_schema import SupplierPurchaseUpdateDTO, StockEntryReadWithCost, SupplierPurchaseBulkDTO
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
    def add_stock_with_cost_average(db: Session, dto:SupplierPurchaseDTO):

        # Criar movimentaÃ§Ã£o
        movement = StockMovement(
            product_id=dto.product_id,
            quantity=dto.quantity,
            movement_type=MovementType.SUPPLIER_PURCHASE,
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
        q = q.order_by(ClientSalesHistory.date.asc())
        items = q.all()
        return [ClientSalesHistoryRead.model_validate(i) for i in items]

    @staticmethod
    def get_client_loss_history_service(
        db: Session,
        cost_center_id: int,
        product_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[ClientLossHistoryRead]:
        q = db.query(ClientLossHistory).filter(ClientLossHistory.cost_center_id == cost_center_id)
        if product_id is not None:
            q = q.filter(ClientLossHistory.product_id == product_id)
        if start_date is not None:
            q = q.filter(ClientLossHistory.date >= start_date)
        if end_date is not None:
            q = q.filter(ClientLossHistory.date <= end_date)
        q = q.order_by(ClientLossHistory.date.asc())
        items = q.all()
        return [ClientLossHistoryRead.model_validate(i) for i in items]

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
