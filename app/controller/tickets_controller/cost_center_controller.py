from . import *

def list_cost_centers(db):
    return CostCenterService.list_cost_centers(db)

def create_cost_center(center_data, db):
    return CostCenterService.create_cost_center_service(db, center_data)

def edit_cost_center(center_id, center_data, db):
    return CostCenterService.edit_cost_center(db, center_id, center_data)

def delete_cost_center(center_id, db):
    return CostCenterService.remove_cost_center(db, center_id)