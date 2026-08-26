from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict


class ServiceBase(BaseModel):
    service_id: int
    client_id: int
    master_id: int


class ServiceCreate(ServiceBase):
    pass  # уже содержит все необходимые поля


class ServiceUpdate(BaseModel):
    is_active: Optional[bool] = None


class ServiceRead(ServiceBase):
    id: int
    service_name: Optional[str] = None
    service_price: Optional[int] = None
    service_time: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
