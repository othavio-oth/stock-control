from . import *
from sqlalchemy.orm import joinedload

def get_all_cost_centers(page,db):
    page_size = 20
    offset = (page - 1) * page_size
    total = db.query(CostCenter).count()
    costcenters = db.query(CostCenter).offset(offset).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size
    return {
        "items": costcenters,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

    

def get_cost_center_by_id(db, center_id):
    costcenter = (
        db.query(CostCenter)
        .options(joinedload(CostCenter.sellers))
        .filter(CostCenter.id == center_id)
        .first()
    )
    return costcenter

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

def get_tickets_by_cost_center(db, center_id):
    return db.query(Ticket).filter(Ticket.cost_center_id == center_id).all()




