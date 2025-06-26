from typing import Optional
from pydantic import BaseModel

class PermissionBase(BaseModel):
    name: str

class PermissionResponse(PermissionBase):
    id: int
    description: str

class PermissionRoleResponse(BaseModel):
    permission_id: int
    role_id: int

class PermissionRequest(BaseModel):
    permission_id: int

class PermissionCreate(PermissionBase):
    description: str
    
class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None