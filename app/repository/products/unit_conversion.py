from . import *

def get_all_conversions(db):
    return db.query(UnitConversion).order_by(UnitConversion.id).all()

def get_conversion_by_id(db, conversion_id):
    return db.query(UnitConversion).filter(UnitConversion.id == conversion_id).first()

def create_conversion(db, conversion_data):
    conversion = UnitConversion(**conversion_data.dict())
    db.add(conversion)
    db.commit()
    db.refresh(conversion)
    return conversion

def update_conversion(db, conversion_id, conversion_data):
    conversion = get_conversion_by_id(db, conversion_id)
    if conversion:
        for key, value in conversion_data.dict().items():
            setattr(conversion, key, value)
        db.commit()
        db.refresh(conversion)
    return conversion

def delete_conversion(db, conversion_id):
    conversion = get_conversion_by_id(db, conversion_id)
    if conversion:
        db.delete(conversion)
        db.commit()
    return conversion