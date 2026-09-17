from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.client import ClientRead
from app.schemas.master import MasterRead
from app.schemas.service import ServiceRead

AppointmentStatus = Literal["pending", "confirmed", "completed", "cancelled"]


class RecordBase(BaseModel):
    start_time: datetime
    end_time: datetime
    master_id: int
    client_id: int
    service_id: int
    comment: Optional[str] = Field(None, max_length=500)


class RecordCreate(RecordBase):
    pass


class RecordUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    master_id: Optional[int] = None
    service_id: Optional[int] = None
    status: Optional[AppointmentStatus] = None
    comment: Optional[str] = Field(None, max_length=500)


class RecordRead(RecordBase):
    id: int
    status: AppointmentStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    master: MasterRead
    client: ClientRead
    service: ServiceRead

    model_config = ConfigDict(from_attributes=True)
