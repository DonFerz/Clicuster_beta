from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.enums import UserRole, MasterPosition
from typing import Optional
from pydantic import ConfigDict


class MasterBase(BaseModel):
    full_name: str
    role: UserRole = UserRole.MASTER
    master_position: MasterPosition
    email: EmailStr
    phone: Optional[str] = None


class MasterCreate(MasterBase):
    password: str


class MasterUpdate(BaseModel):
    full_name: Optional[str] = None
    master_position: Optional[MasterPosition] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class MasterRead(MasterBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
