from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.enums import UserRole
from typing import Optional
from pydantic import ConfigDict


class UserBase(BaseModel):
    full_name: str
    role: UserRole = UserRole.CLIENT
    email: EmailStr
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
