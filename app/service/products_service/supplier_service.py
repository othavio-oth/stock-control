

from app.models.product import Supplier
from app.repository.products.supplier_repository import create_supplier, delete_supplier, get_all_suppliers, get_supplier, update_supplier
from app.schemas.products_schemas.supplier_schema import SupplierSchema


class SupplierService:

    @staticmethod
    def get(db, supplier_id: int):
        return get_supplier(db, supplier_id)

    @staticmethod
    def list(db):
        return get_all_suppliers(db)

    @staticmethod
    def create(db, supplier_data: SupplierSchema):
        supplier = Supplier(
            name=supplier_data.name,
            contact_email=supplier_data.contact_email,
            contact_phone=supplier_data.contact_phone,
            address=supplier_data.address
        )
        return create_supplier(db, supplier)

    @staticmethod
    def update(db, supplier_id: int, supplier_data: SupplierSchema):
        supplier = get_supplier(db, supplier_id)
        if not supplier:
            return None
        update_data = supplier_data.dict(exclude_unset=True)
        return update_supplier(db, supplier, update_data)

    @staticmethod
    def delete(db, supplier_id: int):
        supplier = get_supplier(db, supplier_id)
        if not supplier:
            return False
        delete_supplier(db, supplier)
        return True
