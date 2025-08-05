from app.models.product import RetailChain
from app.repository.products.chain_repository import create_chain, delete_chain, get_all_chains, get_chain_by_id, update_chain

class ChainService:
    @staticmethod
    def list_chains(db):
        return get_all_chains(db)

    @staticmethod
    def create_chain(db, chain_data):
        existing_chain = db.query(RetailChain).filter(RetailChain.name == chain_data.name).first()
        if existing_chain:
            raise ValueError("chain com este name já existe.")
        return create_chain(db, chain_data)

    @staticmethod
    def edit_chain(db, chain_id, chain_data):
        if not get_chain_by_id(db, chain_id):
            raise ValueError("chain não encontrado.")
        return update_chain(db, chain_id, chain_data)

    @staticmethod
    def remove_chain(db, chain_id):
        if not get_chain_by_id(db, chain_id):
            raise ValueError("chain não encontrado.")
        return delete_chain(db, chain_id)