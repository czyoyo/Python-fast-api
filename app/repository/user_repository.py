from typing import Optional
from datetime import datetime, UTC

from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
  def __init__(self, db: Session):
    self.db = db

  def get_by_email(self, email: str)-> Optional[User]:
    return self.db.query(User).filter(User.email == email).first()

  def get_by_nickname(self, nickname: str)-> Optional[User]:
    return self.db.query(User).filter(User.nickname == nickname).first()

  def create(self, user_data: dict) -> User:
    db_user = User(**user_data)
    self.db.add(db_user)
    self.db.commit()
    self.db.refresh(db_user)
    return db_user

  def update(self, user:User)->User:
    user.updated_at = datetime.now(UTC)
    self.db.commit()
    self.db.refresh(user)
    return user
