from typing import Optional, List
from datetime import datetime, UTC
from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy import select



class UserRepository:
  def __init__(self, db: Session):
    self.db = db


  def get_by_id(self, user_id: int) -> Optional[User]:
    return self.db.get(User, user_id)

  def get_by_email(self, email: str)-> Optional[User]:
    return self.db.execute(select(User).where(User.email == email)).scalar_one_or_none()

  def get_by_nickname(self, nickname: str)-> Optional[User]:
    return self.db.execute(
        select(User).where(User.nickname == nickname)
    ).scalar_one_or_none()

  def get_all(self, skip: int = 0, limit: int = 10) -> List[User]:
    return list(
        self.db.execute(
            select(User).offset(skip).limit(limit)
        ).scalars().all()
    )

  def create(self, user: User) -> User:
    self.db.add(user)
    self.db.commit()
    self.db.refresh(user)
    return user

  def update(self, user:User)->User:
    user.updated_at = datetime.now(UTC)
    self.db.commit()
    self.db.refresh(user)
    return user
