from . import *

def get_unit_by_id(db, unit_id):
    return db.query(UnitMeasurement).filter(UnitMeasurement.id == unit_id).first()

def get_all_unit(db):
    return db.query(UnitMeasurement).order_by(UnitMeasurement.id).all()

def create_unit(db, unit_data):
    unit = UnitMeasurement(**unit_data.dict())
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit

def update_unit(db, unit_id, unit_data):
    unit = get_unit_by_id(db, unit_id)
    if unit:
        for key, value in unit_data.dict().items():
            setattr(unit, key, value)
        db.commit()
        db.refresh(unit)
    return unit

def delete_unit(db, unit_id):
    unit = get_unit_by_id(db, unit_id)
    if unit:
        db.delete(unit)
        db.commit()
    return unit