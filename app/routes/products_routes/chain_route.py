from app.controller.products_controller.chain_controller import edit_chain, list_chains
from app.repository.products.chain_repository import create_chain, delete_chain
from app.schemas.products_schemas.retail_chain_schemas import RetailChainResponse
from . import *

router = APIRouter( redirect_slashes=False)

@router.get("/chains", include_in_schema=False)
@router.get("/chains/", response_model=List[RetailChainResponse], tags=["Retail Chain"])
def get_chains(db: Session = Depends(get_db)):
    return list_chains(db)

@router.post("/chains", include_in_schema=False)
@router.post("/chains/", response_model=RetailChainResponse, tags=["Retail Chain"])
def create_new_chain(chain_data: RetailChainBase, db: Session = Depends(get_db)):
    try:
        return create_chain(chain_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/chains/{chain_id}/", include_in_schema=False)
@router.put("/chains/{chain_id}", response_model=RetailChainResponse, tags=["Retail Chain"])
def update_chain(chain_id: int, chain_data: RetailChainBase, db: Session = Depends(get_db)):
    try:
        return edit_chain(chain_id, chain_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/chains/{chain_id}/", include_in_schema=False)
@router.delete("/chains/{chain_id}", tags=["Retail Chain"])
def remove_chain(chain_id: int, db: Session = Depends(get_db)):
    return delete_chain(chain_id, db)
