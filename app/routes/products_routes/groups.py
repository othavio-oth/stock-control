from . import *

router = APIRouter()

@router.get("/groups/", response_model=List[GroupResponse], tags=["Groups"])
def get_groups(db: Session = Depends(get_db)):
    return list_groups(db)

@router.post("/groups/", response_model=GroupResponse, tags=["Groups"])
def create_new_group(group_data: GroupBase, db: Session = Depends(get_db)):
    try:
        return create_group(group_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/groups/{group_id}", response_model=GroupResponse, tags=["Groups"])
def update_group(group_id: int, group_data: GroupBase, db: Session = Depends(get_db)):
    try:
        return edit_group(group_id, group_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/groups/{group_id}", tags=["Groups"])
def remove_group(group_id: int, db: Session = Depends(get_db)):
    return delete_group(group_id, db)