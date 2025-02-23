from datetime import datetime, UTC, timedelta
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import get_password_hash, verify_password, \
  create_access_token
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.services.user_service import UserService


class AuthService:
  def __init__(self, user_service: UserService):
    self.user_service = user_service


  def register_user(self, user_in: UserCreate):
    if self.user_service.get_user_by_email(str(user_in.email)):
      raise HTTPException(
          status_code=400,
          detail="이미 등록된 사용자입니다."
      )
    if self.user_service.get_user_by_nickname(user_in.nickname):
      raise HTTPException(
          status_code=400,
          detail="이미 사용 중인 닉네임입니다."
      )

    user_data = user_in.model_dump() # schema -> dict
    user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    user = User(**user_data)

    create_user = self.user_service.create_user(user)
    # 유저 정보 PRINT
    print(create_user)
    for key, value in create_user.__dict__.items():
      print(f"{key}: {value}")
    return UserResponse.model_validate(create_user)




  def authenticate_user(self, form_data: OAuth2PasswordRequestForm):
      user = self.user_service.get_user_by_email(form_data.username)
      if not user or not verify_password(form_data.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 사용자 이름 또는 비밀번호",
            headers = {"WWW-Authenticate": "Bearer"}
        )

      if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비활성화된 계정입니다."
        )

      access_token_expires = timedelta(
          minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
      scope = ["user", "admin"] if user.is_superuser else ["user"]

      access_token = create_access_token(
          data={"sub": user.email},
          expires_delta=access_token_expires,
          scopes=scope
      )

      return Token(
          access_token=access_token,
          token_type="bearer",
          expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
      )

