from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.schemas.token import Token
from app.schemas.user import UserResponse, UserCreate
from database import get_db
from app.crud.user import user_crud
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(
    user_in: UserCreate,
    db: Annotated[Session, Depends(get_db)]
):
  """새로운 사용자 등록"""
  if user_crud.get_user_by_email(db, email=user_in.email):
    raise HTTPException(
        status_code=400,
        detail="이미 등록된 사용자입니다."
    )
  if user_crud.get_user_by_nickname(db, nickname=user_in.nickname):
    raise HTTPException(
        status_code=400,
        detail="이미 사용 중인 닉네임입니다."
    )
  try:
    user = user_crud.create_user(db, user_in)
    print("최종 반환 전 유저 출력", user)
    return user
  except ValueError as e:
    raise HTTPException(
        status_code=400,
        detail=str(e)
    )

@router.post("/login", response_model=Token)
def login(
    db: Annotated[Session, Depends(get_db)],
    from_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
  """사용자 로그인 및 액세스 토큰 발급"""
  user = user_crud.authenticate(
      db, username=from_data.username, password=from_data.password
  )
  if not user:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="잘못된 사용자 이름 또는 비밀번호",
        headers={"WWW-Authenticate": "Bearer"}
    )
  if not user_crud.is_active(user):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="비활성화된 계정입니다."
    )

  access_token_expires = timedelta(
      minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
  )

  # 사용자 권한에 따른 스코프 설정
  scope = ["user"]
  if user_crud.is_superuser(user):
    scope.append("admin")

  access_token = create_access_token(
      data={"sub": user.email}, expires_delta=access_token_expires, scopes=scope
  )
  return Token(
      access_token=access_token,
      token_type="bearer",
      expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
  )
