from datetime import datetime, UTC, timedelta
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.core.config import settings
from app.core.security import get_password_hash, verify_password, \
  create_access_token
from app.repository.user_repository import UserRepository
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse


class AuthService:
  def __init__(self, user_repository: UserRepository):
    self.user_repository = user_repository


  def register_user(self, user_in: UserCreate):
    if self.user_repository.get_by_email(str(user_in.email)):
      raise HTTPException(
          status_code=400,
          detail="이미 등록된 사용자입니다."
      )
    if self.user_repository.get_by_nickname(user_in.nickname):
      raise HTTPException(
          status_code=400,
          detail="이미 사용 중인 닉네임입니다."
      )

    user_data = user_in.model_dump() # schema -> dict
    user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    user_data["is_superuser"] = False
    user_data["created_at"] = datetime.now(UTC)
    user_data["updated_at"] = datetime.now(UTC)

    create = self.user_repository.create(user_data)

    return UserResponse.model_validate(create)




  def authenticate_user(self, form_data: OAuth2PasswordRequestForm):
      user = self.user_repository.get_by_email(form_data.username)
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

