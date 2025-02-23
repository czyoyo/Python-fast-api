from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.repository.user_repository import UserRepository
from app.schemas.token import Token
from app.schemas.user import UserResponse, UserCreate
from app.service.auth_service import AuthService
from database import get_db

router = APIRouter()

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
  user_repository = UserRepository(db)
  return AuthService(user_repository)

@router.get('/test')
def test():
  return {"test": "test"}

@router.post("/register", response_model=UserResponse)
def register(
    user_in: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
  print("@@@@@@@@@@@@@@@")
  """새로운 사용자 등록"""
  return auth_service.register_user(user_in)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
  """사용자 로그인 및 액세스 토큰 발급"""
  return auth_service.authenticate_user(form_data)
