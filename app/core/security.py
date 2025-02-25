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


def create_access_token(sub: int, expires_delta: timedelta | None = None,
    scopes: list[str] | None = None) -> str:
  """Access 토큰을 생성합니다."""
  if expires_delta:
    expire = datetime.now(UTC) + expires_delta
  else:
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

  # datetime을 int로 변환
  expire_timestamp = expire.timestamp()

  # sub 값이 str이 아닌 경우 str로 변환
  to_encode = {"exp": expire_timestamp, "sub": str(sub)}

  if scopes:
    to_encode["scopes"] = scopes

  encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY,
                           algorithm=settings.ALGORITHM)
  return encoded_jwt



def decode_token(token: str) -> TokenPayload:
  try:
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    token_payload = TokenPayload(
        sub=payload.get("sub"),
        scopes=payload.get("scopes", [])
    )
    return token_payload

  except jwt.JWTError as e:
    print(f"JWT 디코딩 에러: {str(e)}")
    raise
  except Exception as e:
    print(f"기타 예외 발생: {str(e)}")
    print(f"예외 타입: {type(e)}")
    raise



