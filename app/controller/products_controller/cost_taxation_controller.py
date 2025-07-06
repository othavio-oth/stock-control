from . import *

def list_cost_taxations(db):
    return CostTaxationService.list_cost_taxations(db)

def create_cost_taxation(cost_data, db):
    return CostTaxationService.create_cost_taxation(db, cost_data)

def edit_cost_taxation(cost_id, cost_data, db):
    return CostTaxationService.edit_cost_taxation(db, cost_id, cost_data)

def delete_cost_taxation(cost_id, db):
    return CostTaxationService.remove_cost_taxation(db, cost_id)