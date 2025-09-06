from . import *

router = APIRouter(redirect_slashes=False)

@router.get("/conversions/", response_model=List[ConversionResponse], tags=["Conversions"])
def get_conversions(db: Session = Depends(get_db)):
    return list_conversions(db)

@router.get("/conversions/{conversion_id}", response_model=ConversionResponse, tags=["Conversions"])
def get_conversion(conversion_id: int, db: Session = Depends(get_db)):
    return get_conversion_by_id(conversion_id, db)

@router.post("/conversions/", response_model=ConversionResponse, tags=["Conversions"])
def create_new_conversion(conversion_data: ConversionCreate, db: Session = Depends(get_db)):
    return create_conversion(conversion_data, db)

@router.put("/conversions/{conversion_id}", response_model=ConversionResponse, tags=["Conversions"])
def update_conversion(conversion_id: int, conversion_data: ConversionUpdate, db: Session = Depends(get_db)):
    try:
        return edit_conversion(conversion_id, conversion_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/conversions/{conversion_id}", tags=["Conversions"])
def remove_conversion(conversion_id: int, db: Session = Depends(get_db)):
    return delete_conversion(conversion_id, db)