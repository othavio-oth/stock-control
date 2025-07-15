from app.schemas.users_schemas.seller_schema import SellerCreate
from app.service.seller_service.seller_service import SellerService
from . import *

def create_seller(seller_data: SellerCreate, db:Session = Depends(get_db)):
    try:
        return SellerService.create_new_seller(db, seller_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
def update_seller(seller_id: int, seller_data: SellerCreate, db: Session = Depends(get_db)):
    try:
        return SellerService.update_seller(db, seller_id, seller_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def delete_seller(seller_id: int, db: Session = Depends(get_db)):
    try:
        return SellerService.delete_seller(db, seller_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))