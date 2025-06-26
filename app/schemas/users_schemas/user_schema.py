from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    nickname: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    date_joined: Optional[datetime] = None  # Aceita None como valor
    last_login: Optional[datetime] = None  # Aceita None como valor

    class Config:
        from_attributes = True  # Permite trabalhar diretamente com objetos do ORM

class UserResponseList(UserResponse):
    roles: str