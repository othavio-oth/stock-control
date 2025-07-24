from . import *

router = APIRouter()

@router.get("/type_registrations/", response_model=List[TypeRegistrationResponse], tags=["Type Registrations"])
def get_type_registrations(db: Session = Depends(get_db)):
    return list_type_registrations(db)

@router.post("/type_registrations/", response_model=TypeRegistrationResponse, tags=["Type Registrations"])
def create_new_type_registration(type_registration_data: TypeRegistrationCreate, db: Session = Depends(get_db)):
    try:
        return create_type_registration(type_registration_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/type_registrations/{type_registration_id}", response_model=TypeRegistrationResponse,tags=["Type Registrations"] )
def update_type_registration(type_registration_id: int, type_registration_data: TypeRegistrationUpdate, db: Session = Depends(get_db)):
    try:
        return edit_type_registration(type_registration_id, type_registration_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/type_registrations/{type_registration_id}", tags=["Type Registrations"])
def remove_type_registration(type_registration_id: int, db: Session = Depends(get_db)):
    return delete_type_registration(type_registration_id, db)