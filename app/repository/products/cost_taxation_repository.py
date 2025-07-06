from . import *

def get_all_cost_taxations(db):
    return db.query(CostTaxation).order_by(CostTaxation.id).all()

def get_cost_taxation_by_id(db, cost_id):
    return db.query(CostTaxation).filter(CostTaxation.id == cost_id).first()

def create_cost_taxation(db, cost_data):
    cost = CostTaxation(**cost_data.dict())
    db.add(cost)
    db.commit()
    db.refresh(cost)
    return cost

def update_cost_taxation(db, cost_id, cost_data):
    cost = get_cost_taxation_by_id(db, cost_id)
    if cost:
        for key, value in cost_data.dict().items():
            setattr(cost, key, value)
        db.commit()
        db.refresh(cost)
    return cost

def delete_cost_taxation(db, cost_id):
    cost = get_cost_taxation_by_id(db, cost_id)
    if cost:
        db.delete(cost)
        db.commit()
    return cost