from app.models.product import UnitMeasurement
from app.repository.products.unit_measurement_repository import create_unit, delete_unit, get_unit_by_id, update_unit, get_all_unit

class UnitMeasurementService:
    @staticmethod
    def list_units(db):
        return get_all_unit(db)

    @staticmethod
    def create_unit(db, unit_data):
        existing_unit = db.query(UnitMeasurement).filter(UnitMeasurement.name == unit_data.name).first()
        if existing_unit:
            raise ValueError("Unit de Medida com este nome já existe.")
        return create_unit(db, unit_data)

    @staticmethod
    def edit_unit(db, unit_id, unit_data):
        if not get_unit_by_id(db, unit_id):
            raise ValueError("Unit de Medida não encontrada.")
        return update_unit(db, unit_id, unit_data)

    @staticmethod
    def remove_unit(db, unit_id):
        if not get_unit_by_id(db, unit_id):
            raise ValueError("Unit de Medida não encontrada.")
        return delete_unit(db, unit_id)