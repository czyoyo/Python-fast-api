from fastapi import Depends
from sqlalchemy.orm import Session

from app.repository.user_repository import UserRepository
from app.service.auth_service import AuthService
from app.service.user_service import UserService
from database import get_db


# Repository 의존성
def get_user_repository(
  db: Session = Depends(get_db)
) -> UserRepository:
  return UserRepository(db)

# Service 의존성
def get_user_service(
  user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
  return UserService(user_repository)

def get_auth_service(
    user_service: UserService = Depends(get_user_service)
) -> AuthService:
  return AuthService(user_service)
