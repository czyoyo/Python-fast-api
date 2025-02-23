from typing import Optional, List

from app.repository.user_repository import UserRepository
from app.models.user import User


class UserService:
  def __init__(self, user_repository: UserRepository):
    self.user_repository = user_repository

  def get_user_by_id(self, user_id: int) -> Optional[User]:
    return self.user_repository.get_by_id(user_id)

  def get_user_by_email(self, email: str) -> Optional[User]:
    return self.user_repository.get_by_email(email)

  def get_users(self, skip: int = 0, limit: int = 10) -> List[User]:
    return self.user_repository.get_all(skip=skip, limit=limit)

  def create_user(self, user: User) -> User:
    return self.user_repository.create(user)

  def get_user_by_nickname(self, nickname: str) -> Optional[User]:
    return self.user_repository.get_by_nickname(nickname)
