# app/services/stock_movement_service.py (ou onde concentra seus services)

from datetime import datetime, time
from sqlalchemy.orm import Session
from app.schemas.stock_schemas.stock_movement_schema import RegisterClientSalesDTO
from app.repository.stock.stock_movement_repository import (
    get_or_create_client_stock_for_update,
    decrement_client_stock,
    upsert_sales_for_day,
    create_client_sale_movement,
)

class ProductSalesService:

    @staticmethod
    def register_client_sales_simple(db: Session, payload: RegisterClientSalesDTO):
        """
        Registra vendas do cliente em UM ÚNICO DIA (idempotente por somar no dia):
        - Soma em ClientSalesHistory (upsert + incremento)
        - Cria StockMovement CLIENT_SALE com created_at = 00:00 do 'registration_date'
        - Debita ClientStock (sem permitir negativo)
        """
        # 1) Valida data (não lançar no futuro)
        today = datetime.now().date()
        if payload.registration_date > today:
            raise ValueError("A 'registration_date' não pode ser futura.")

        # 2) Estoque do cliente com lock
        cs = get_or_create_client_stock_for_update(
            db,
            cost_center_id=payload.cost_center_id,
            product_id=payload.product_id,
        )

        # 3) Não permitir negativo por padrão
        total = int(payload.total_sold)
        if cs.quantity < total:
            raise ValueError(
                f"Estoque insuficiente no cliente. Em estoque: {cs.quantity}, vendido: {total}"
            )

        # 4) Upsert + incremento na venda do dia
        upsert_sales_for_day(
            db,
            cost_center_id=payload.cost_center_id,
            product_id=payload.product_id,
            d=payload.registration_date,
            qty=total,
        )

        # 5) Movement (created_at = início do dia)
        created_at = datetime.combine(payload.registration_date, time.min)
        create_client_sale_movement(
            db,
            product_id=payload.product_id,
            cost_center_id=payload.cost_center_id,
            qty=total,
            created_at=created_at,
            product_unit_cost=None,   
        )

        # 6) Baixa no estoque do cliente
        decrement_client_stock(cs, total, allow_negative=False)

        # 7) Commit
        db.commit()

        return {
            "cost_center_id": payload.cost_center_id,
            "product_id": payload.product_id,
            "registration_date": str(payload.registration_date),
            "applied": total,
            "message": "Venda registrada com sucesso.",
        }
