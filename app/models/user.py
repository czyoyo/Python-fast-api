from pydantic import EmailStr
from sqlalchemy import Column, Integer, String
from app.db.database import Base

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  email = Column(EmailStr, unique=True, index=True)
  name = Column(String)
  password = Column(String)
