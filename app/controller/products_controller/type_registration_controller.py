from . import *

def list_type_registrations(db):
    return TypeRegistrationService.list_type_registrations(db)

def create_type_registration(type_registration_data, db):
    return TypeRegistrationService.create_type_registration(db, type_registration_data)

def edit_type_registration(type_registration_id, type_registration_data, db):
    return TypeRegistrationService.edit_type_registration(db, type_registration_id, type_registration_data)

def delete_type_registration(type_registration_id, db):
    return TypeRegistrationService.remove_type_registration(db, type_registration_id)