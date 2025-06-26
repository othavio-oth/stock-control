from . import *

def list_conversions(db):
    return ConversionService.list_conversions(db)

def get_conversion_by_id(conversion_id, db):
    return ConversionService.get_conversion_by_id_service(db, conversion_id)

def create_conversion(conversion_data, db):
    return ConversionService.create_conversion(db, conversion_data)

def edit_conversion(conversion_id, conversion_data, db):
    return ConversionService.edit_conversion(db, conversion_id, conversion_data)

def delete_conversion(conversion_id, db):
    return ConversionService.remove_conversion(db, conversion_id)