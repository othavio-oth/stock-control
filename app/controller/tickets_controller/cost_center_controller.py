from . import *

def list_cost_centers(page,db):
    return CostCenterService.list_cost_centers(page,db)

def create_cost_center(center_data, db):
    return CostCenterService.create_cost_center_service(db, center_data)

def edit_cost_center(center_id, center_data, db):
    return CostCenterService.edit_cost_center(db, center_id, center_data)

def delete_cost_center(center_id, db):
    return CostCenterService.remove_cost_center(db, center_id)

def get_tickets_by_cost_center(center_id, db):
    return CostCenterService.get_tickets_by_cost_center(db, center_id)

def get_cost_center_by_id(center_id, db):
    return CostCenterService.get_cost_center_by_id(db, center_id)

def get_ticket_products_by_cost_center(db, cost_center_id):
    return CostCenterService.get_ticket_products_by_cost_center(db, cost_center_id)

def search_cost_centers_by_term_controller(term, page, db):
    return CostCenterService.search_cost_centers(term, page, db)