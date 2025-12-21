from app.models.seller import Seller
from . import *

def create_seller(seller_data, db) -> Seller:
    seller = Seller(**seller_data.dict())
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller


def edit_seller(db, seller_id, seller_data):
    seller = db.query(Seller).filter(Seller.id == seller_id).first()
    if not seller:
        raise ValueError("Vendedor não encontrado.")
    for key, value in seller_data.dict().items():
        setattr(seller, key, value)
    db.commit()
    db.refresh(seller)
    return seller

def delete_seller(db, seller_id):
    seller = db.query(Seller).filter(Seller.id == seller_id).first()
    if not seller:
        raise ValueError("Vendedor não encontrado.")
    db.delete(seller)
    db.commit()
    return seller