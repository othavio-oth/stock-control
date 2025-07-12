from pydantic import BaseModel
from app.schemas.tickets_schemas.cost_center_schemas import CostCenterResponse
from app.schemas.users_schemas.user_schema import UserResponse


class SellerBase(BaseModel):
    cost_center_id: int

class SellerCreate(SellerBase):
    user_id: int

class SellerResponse(SellerBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class SellerWithUser(SellerResponse):
    user: UserResponse
    cost_center: CostCenterResponse

    class Config:
        from_attributes = True