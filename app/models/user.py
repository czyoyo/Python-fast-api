from sqlalchemy import Integer, String, Boolean, DateTime, Nullable
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC
from sqlalchemy.sql import func


from database import Base

class User(Base):
  __tablename__ = "user"
  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
  email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
  nickname:Mapped[str] = mapped_column(String, index=True, nullable=False)
  hashed_password:Mapped[str] = mapped_column(String, nullable=False)
  is_active:Mapped[bool] = mapped_column(Boolean, default=True)
  is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
