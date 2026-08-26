from pydantic import BaseModel
from app.models.enums import SalonType
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict


class SalonBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    type: SalonType


class SalonCreate(SalonBase):
    owner_id: int  # ID пользователя-администратора


class SalonUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    type: Optional[SalonType] = None
    is_active: Optional[bool] = None


class SalonRead(SalonBase):
    id: int
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
