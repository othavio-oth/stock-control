from pydantic import BaseModel

class SupplierSchema(BaseModel):
    name: str
    contact_email: str | None = None
    contact_phone: str | None = None
    address: str | None = None
    

    class Config:
        from_attributes = True  # Permite conversão de/para ORM

class SupplierCreate(SupplierSchema):
    pass
        
class SupplierReponse(SupplierSchema):
    id: int

    class Config:
        from_attributes = True
        
class SupplierUpdate(SupplierSchema):
    id: int
    