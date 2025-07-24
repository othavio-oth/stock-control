from . import *

router = APIRouter()

@router.get("/units/", response_model=List[UnitMeasurementResponse], tags=["Units"]) 
def get_all_units(db: Session = Depends(get_db)):
    return list_unit_measurement(db)

@router.post("/units/", response_model=UnitMeasurementResponse, tags=["Units"])
def create_new_unit(unit_data: UnitMeasurementBase, db: Session = Depends(get_db)):
    try:
        return create_unit_measurement(unit_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/units/{unit_id}", response_model=UnitMeasurementResponse,tags=["Units"])
def update_unit(unit_id: int, unit_data: UnitMeasurementBase, db: Session = Depends(get_db)):
    try:
        return edit_unit_measurement(unit_id, unit_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/units/{unit_id}", tags=["Units"])
def remove_unit(unit_id: int, db: Session = Depends(get_db)):
    return delete_unit_measurement(unit_id, db)