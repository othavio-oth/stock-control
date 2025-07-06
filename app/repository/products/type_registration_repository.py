from . import *

def get_all_type_registrations(db):
    return db.query(TypeRegistration).order_by(TypeRegistration.id).all()

def get_type_registration_by_id(db, type_registration_id):
    return db.query(TypeRegistration).filter(TypeRegistration.id == type_registration_id).first()

def create_type_registration(db, type_registration_data):
    type_registration = TypeRegistration(**type_registration_data.dict())
    db.add(type_registration)
    db.commit()
    db.refresh(type_registration)
    return type_registration

def update_type_registration(db, type_registration_id, type_registration_data):
    type_registration = get_type_registration_by_id(db, type_registration_id)
    if type_registration:
        for key, value in type_registration_data.dict().items():
            setattr(type_registration, key, value)
        db.commit()
        db.refresh(type_registration)
    return type_registration

def delete_type_registration(db, type_registration_id):
    type_registration = get_type_registration_by_id(db, type_registration_id)
    if type_registration:
        db.delete(type_registration)
        db.commit()
    return type_registration