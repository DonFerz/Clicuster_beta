from sqlalchemy import String, ForeignKey, Integer, DateTime, func, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .salon import Salon
    from .master import Master
    from .appointment import Appointment


master_services = Table(
    "master_services",
    Base.metadata,
    Column("master_id", ForeignKey("masters.id"), primary_key=True),
    Column("service_id", ForeignKey("services.id"), primary_key=True),
)

class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    salon_id: Mapped[int] = mapped_column(ForeignKey("salons.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)  # длительность в минутах
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # цена в копейках/центах (целое число)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    salon: Mapped["Salon"] = relationship(back_populates="services")
    masters: Mapped[list["Master"]] = relationship(
        secondary="master_services",
        back_populates="services"
    )
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="service")
