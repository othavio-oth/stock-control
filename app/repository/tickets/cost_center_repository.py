from . import *

def get_all_cost_centers(db):
    return db.query(CostCenter).all()

def get_cost_center_by_id(db, center_id):
    return db.query(CostCenter).filter(CostCenter.id == center_id).first()

def create_cost_center(db, center_data):
    center = CostCenter(**center_data.dict())
    db.add(center)
    db.commit()
    db.refresh(center)
    return center

def update_cost_center(db, center_id, center_data):
    center = get_cost_center_by_id(db, center_id)
    if center:
        for key, value in center_data.dict().items():
            setattr(center, key, value)
        db.commit()
        db.refresh(center)
    return center

def delete_cost_center(db, center_id):
    center = get_cost_center_by_id(db, center_id)
    if center:
        db.delete(center)
        db.commit()
    return center