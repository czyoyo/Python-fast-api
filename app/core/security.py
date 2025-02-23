from typing import Optional, Annotated
from datetime import datetime, timedelta, UTC

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from .config import settings
from ..schemas.token import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    scopes={
      "admin": "Admin access",
      "user": "User access"
    },
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
  return pwd_context.hash(password)


def create_access_token(sub: str, expires_delta: timedelta | None = None,
    scopes: list[str] | None = None) -> str:
  """Access 토큰을 생성합니다."""
  if expires_delta:
    expire = datetime.now(UTC) + expires_delta
  else:
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

  to_encode = {"exp": expire, "sub": sub}
  if scopes:
    to_encode["scopes"] = scopes

  encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY,
                           algorithm=settings.ALGORITHM)
  return encoded_jwt



def decode_token(token: str) -> TokenPayload:
  """토큰을 디코딩하고 페이로드를 반환합니다."""
  payload = jwt.decode(
      token,
      settings.SECRET_KEY,
      algorithms=[settings.ALGORITHM]
  )
  return TokenPayload(**payload)

