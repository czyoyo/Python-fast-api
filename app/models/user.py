from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped
from datetime import datetime, UTC

from database import Base

class User(Base):
  __tablename__ = "user"
  id: Mapped[int] = Column(Integer, primary_key=True, index=True)
  email:Mapped[EmailStr] = Column(EmailStr, unique=True, index=True)
  nickname:Mapped[str] = Column(String, index=True)
  hashed_password:Mapped[str] = Column(String, nullable=False)
  is_active:Mapped[bool] = Column(Boolean, default=True)
  is_superuser: Mapped[bool] = Column(Boolean, default=False)
  created_at: Mapped[datetime] = Column(DateTime, default=datetime.now(UTC))
  updated_at: Mapped[datetime] = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
