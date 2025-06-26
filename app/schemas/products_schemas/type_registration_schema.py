from pydantic import BaseModel
from typing import Optional

class TypeRegistrationBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: bool = True

class TypeRegistrationCreate(TypeRegistrationBase):
    pass

class TypeRegistrationUpdate(TypeRegistrationBase):
    pass

class TypeRegistrationResponse(TypeRegistrationBase):
    id: int