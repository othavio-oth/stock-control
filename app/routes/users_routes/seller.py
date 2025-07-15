from app.controller.users_controller.seller_controller import delete_seller, update_seller
from app.repository.seller.seller_repository import create_seller
from app.schemas.users_schemas.seller_schema import SellerCreate, SellerResponse
from . import *

router = APIRouter()

@router.post("/", response_model=SellerResponse)
def create_new_seller(seller: SellerCreate, db: Session = Depends(get_db)):
    return create_seller(seller, db)

@router.put("/{seller_id}", response_model=SellerResponse)
def update_seller_details(seller_id: int, seller: SellerCreate, db: Session = Depends(get_db)):
    return update_seller(seller_id, seller, db) 

@router.delete("/{seller_id}")
def delete_seller_by_id(seller_id: int, db: Session = Depends(get_db)):
    return delete_seller(seller_id, db)