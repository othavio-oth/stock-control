from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.product import ShelfPrice
from app.repository.products.shelf_price_repository import (
    create_shelf_price,
    delete_shelf_price,
    get_shelf_price_by_id,
    list_shelf_prices,
    update_shelf_price,
)
from app.schemas.products_schemas.shelf_price_schema import ShelfPriceCreate, ShelfPriceUpdate


class ShelfPriceService:
    @staticmethod
    def _validate_scope(cost_center_id: Optional[int], retail_chain_id: Optional[int]) -> None:
        if cost_center_id and retail_chain_id:
            raise ValueError("Informe apenas cost_center_id OU retail_chain_id.")
        if not cost_center_id and not retail_chain_id:
            raise ValueError("É necessário informar cost_center_id ou retail_chain_id.")

    @staticmethod
    def create(db: Session, data: ShelfPriceCreate) -> ShelfPrice:
        ShelfPriceService._validate_scope(data.cost_center_id, data.retail_chain_id)
        return create_shelf_price(db, data.model_dump(exclude_none=True))

    @staticmethod
    def list(
        db: Session,
        *,
        product_id: Optional[int] = None,
        cost_center_id: Optional[int] = None,
        retail_chain_id: Optional[int] = None,
    ) -> List[ShelfPrice]:
        return list_shelf_prices(
            db,
            product_id=product_id,
            cost_center_id=cost_center_id,
            retail_chain_id=retail_chain_id,
        )

    @staticmethod
    def get_by_id(db: Session, shelf_price_id: int) -> Optional[ShelfPrice]:
        return get_shelf_price_by_id(db, shelf_price_id)

    @staticmethod
    def update(db: Session, shelf_price_id: int, data: ShelfPriceUpdate) -> Optional[ShelfPrice]:
        ShelfPriceService._validate_scope(data.cost_center_id, data.retail_chain_id) if (
            data.cost_center_id is not None or data.retail_chain_id is not None
        ) else None
        payload = data.model_dump(exclude_none=True)
        return update_shelf_price(db, shelf_price_id, payload)

    @staticmethod
    def delete(db: Session, shelf_price_id: int) -> bool:
        return delete_shelf_price(db, shelf_price_id)
