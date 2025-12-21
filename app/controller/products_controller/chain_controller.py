from app.service.products_service.chains_service import ChainService
from . import *

def list_chains(db):
    return ChainService.list_chains(db)

def create_chain(chain_data, db):
    return ChainService.create_chain(db, chain_data)

def edit_chain(chain_id, chain_data, db):
    return ChainService.edit_chain(db, chain_id, chain_data)

def delete_chain(chain_id, db):
    return ChainService.remove_chain(db, chain_id)