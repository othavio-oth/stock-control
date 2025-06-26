from . import *

def list_unit_measurement(db):
    return UnitMeasurementService.list_units(db)

def create_unit_measurement(unit_data, db):
    return UnitMeasurementService.create_unit(db, unit_data)

def edit_unit_measurement(unit_id, unit_data, db):
    return UnitMeasurementService.edit_unit(db, unit_id, unit_data)

def delete_unit_measurement(unit_id, db):
    return UnitMeasurementService.remove_unit(db, unit_id)