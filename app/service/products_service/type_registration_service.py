from app.repository.products.type_registration_repository import create_type_registration, update_type_registration, get_all_type_registrations, get_type_registration_by_id, delete_type_registration
from app.models.groups import TypeRegistration

class TypeRegistrationService:
    @staticmethod
    def list_type_registrations(db):
        return get_all_type_registrations(db)

    @staticmethod
    def create_type_registration(db, type_registration_data):
        existing_type = db.query(TypeRegistration).filter(TypeRegistration.name == type_registration_data.name).first()
        if existing_type:
            raise ValueError("Tipo de Registro com este nome já existe.")
        return create_type_registration(db, type_registration_data)

    @staticmethod
    def edit_type_registration(db, type_registration_id, type_registration_data):
        if not get_type_registration_by_id(db, type_registration_id):
            raise ValueError("Tipo de Registro não encontrado.")
        return update_type_registration(db, type_registration_id, type_registration_data)

    @staticmethod
    def remove_type_registration(db, type_registration_id):
        if not get_type_registration_by_id(db, type_registration_id):
            raise ValueError("Tipo de Registro não encontrado.")
        return delete_type_registration(db, type_registration_id)