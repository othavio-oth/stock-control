from app.repository.products.unit_conversion import get_all_conversions, get_conversion_by_id, create_conversion, update_conversion, delete_conversion

class ConversionService:
    @staticmethod
    def list_conversions(db):
        return get_all_conversions(db)
    
    @staticmethod
    def get_conversion_by_id_service(db, conversion_id):
        return get_conversion_by_id(db, conversion_id)

    @staticmethod
    def create_conversion(db, conversion_data):
        return create_conversion(db, conversion_data)

    @staticmethod
    def edit_conversion(db, conversion_id, conversion_data):
        if not get_conversion_by_id(db, conversion_id):
            raise ValueError("Conversão não encontrada.")
        return update_conversion(db, conversion_id, conversion_data)

    @staticmethod
    def remove_conversion(db, conversion_id):
        if not get_conversion_by_id(db, conversion_id):
            raise ValueError("Conversão não encontrada.")
        return delete_conversion(db, conversion_id)