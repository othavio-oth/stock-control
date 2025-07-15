from http.client import HTTPException
from app.models.seller import Seller
from app.models.user import User
from app.repository.seller.seller_repository import create_seller, delete_seller, edit_seller


class SellerService:
    
 from fastapi import HTTPException

class SellerService:
    
    @staticmethod
    def create_new_seller( seller_data, db):
        try:
           seller = create_seller(db, seller_data)
           return seller
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


    @staticmethod
    def update_seller(db, seller_id, seller_data):
        try:
            seller = edit_seller(db, seller_id, seller_data)
            return seller
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    def delete_seller(db, seller_id):
        try:
            seller = delete_seller(db, seller_id)
            return seller
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))