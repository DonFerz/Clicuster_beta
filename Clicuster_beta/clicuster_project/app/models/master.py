from sqlalchemy import String, Enum, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
from .enums import MasterPosition
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import User
    from .salon import Salon
    from .service import Service
    from .appointment import Appointment


class Master(Base):
    __tablename__ = "masters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)  # один пользователь - один мастер
    salon_id: Mapped[int] = mapped_column(ForeignKey("salons.id"), nullable=False)
    position: Mapped[MasterPosition] = mapped_column(Enum(MasterPosition), default=MasterPosition.MASTER)
    description: Mapped[str] = mapped_column(String(500), nullable=True)  # описание мастера
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    user: Mapped["User"] = relationship(back_populates="master_profile")
    salon: Mapped["Salon"] = relationship(back_populates="masters")
    # У мастера могут быть услуги (многие ко многим через промежуточную таблицу)
    services: Mapped[list["Service"]] = relationship(
        secondary="master_services",
        back_populates="masters"
    )
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="master")
