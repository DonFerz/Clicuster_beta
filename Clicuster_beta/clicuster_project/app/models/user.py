from sqlalchemy import String, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .enums import UserRole
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .salon import Salon
    from .appointment import Appointment
    from .master import Master


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.CLIENT)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    salons: Mapped[list["Salon"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="client")
    master_profile: Mapped["Master"] = relationship(back_populates="user", uselist=False)
