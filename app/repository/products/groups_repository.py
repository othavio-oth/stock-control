from . import *

def get_all_groups(db):
    return db.query(Group).order_by(Group.id).all()

def get_group_by_id(db, group_id):
    return db.query(Group).filter(Group.id == group_id).first()

def create_group(db, group_data):
    group = Group(**group_data.dict())
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

def update_group(db, group_id, group_data):
    group = get_group_by_id(db, group_id)
    if group:
        for key, value in group_data.dict().items():
            setattr(group, key, value)
        db.commit()
        db.refresh(group)
    return group

def delete_group(db, group_id):
    group = get_group_by_id(db, group_id)
    if group:
        db.delete(group)
        db.commit()
    return group