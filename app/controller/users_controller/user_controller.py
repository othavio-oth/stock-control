from . import *

def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_new_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def list_users(db: Session = Depends(get_db)):
    try:
        result = service_list_users(db)
        logging.info(result)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return get_user_details(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        return modify_user(db, user_id, user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        remove_user(db, user_id)
        return {"detail": "Usuário deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
