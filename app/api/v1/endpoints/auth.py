from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies.services import get_auth_service
from app.schemas.token import Token
from app.schemas.user import UserResponse, UserCreate
from app.services.auth_service import AuthService

router = APIRouter()



@router.get('/test')
def test():
  return {"test": "test"}

@router.post("/register", response_model=UserResponse)
def register(
    user_in: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:
  """새로운 사용자를 등록합니다."""
  return auth_service.register_user(user_in)

@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(get_auth_service)
) -> Token:
  """사용자 로그인 및 액세스 토큰 발급"""
  return auth_service.authenticate_user(form_data)
