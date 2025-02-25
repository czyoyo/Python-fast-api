from typing import Optional, List

from fastapi import HTTPException, status

from app.repository.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserResponse


class UserService:
  def __init__(self, user_repository: UserRepository):
    self.user_repository = user_repository

  def get_user_info(self, user_id: int) -> Optional[UserResponse]:
    user = self.user_repository.get_by_id(user_id)
    if not user:
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="사용자를 찾을 수 없습니다"
      )

    return UserResponse.model_validate(user)



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
