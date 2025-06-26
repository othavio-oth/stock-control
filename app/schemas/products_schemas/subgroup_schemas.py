from pydantic import BaseModel
from typing import Optional

class SubGroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: bool = True

class SubGroupCreate(SubGroupBase):
    pass

class SubGroupUpdate(SubGroupBase):
    pass

class SubGroupResponse(SubGroupBase):
    id: int