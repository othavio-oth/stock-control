from app.models.product import RetailChain
from . import *
from sqlalchemy.orm import joinedload

def get_all_chains(db):
    return db.query(RetailChain).options(joinedload(RetailChain.cost_centers)).order_by(RetailChain.id).all()

def get_chain_by_id(db, chain_id):
    return db.query(RetailChain).filter(RetailChain.id == chain_id).options(joinedload(RetailChain.cost_centers)).first()

def create_chain(db, chain_data):
    chain = RetailChain(**chain_data.dict())
    db.add(chain)
    db.commit()
    db.refresh(chain)
    return chain

def update_chain(db, chain_id, chain_data):
    chain = get_chain_by_id(db, chain_id)
    if chain:
        for key, value in chain_data.dict().items():
            setattr(chain, key, value)
        db.commit()
        db.refresh(chain)
    return chain

def delete_chain(db, chain_id):
    chain = get_chain_by_id(db, chain_id)
    if chain:
        db.delete(chain)
        db.commit()
    return chain