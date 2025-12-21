from app.models.product import Supplier


def get_supplier(db, supplier_id: int):
        return db.query(Supplier).filter(Supplier.id == supplier_id).first()

def get_all_suppliers(db):
    return db.query(Supplier).all()

def create_supplier(db, supplier: Supplier):
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

def update_supplier(db, supplier: Supplier, update_data: dict):
    for key, value in update_data.items():
        setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return supplier

def delete_supplier(db, supplier: Supplier):
    db.delete(supplier)
    db.commit()