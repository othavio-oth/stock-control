from typing import Optional
from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleResponse(RoleBase):
    id: int

class RoleUserResponse(BaseModel):    
    user_id: int
    role_id: int

class RoleRequest(BaseModel):
    user_id: int