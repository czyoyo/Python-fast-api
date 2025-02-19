from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC

from database import Base

class User(Base):
  __tablename__ = "user"
  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
  email: Mapped[EmailStr] = mapped_column(String, unique=True, index=True)
  nickname:Mapped[str] = mapped_column(String, index=True)
  hashed_password:Mapped[str] = mapped_column(String, nullable=False)
  is_active:Mapped[bool] = mapped_column(Boolean, default=True)
  is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
  updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
