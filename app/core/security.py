from typing import Optional, Annotated
from datetime import datetime, timedelta, UTC

from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
from .config import settings
from ..models.user import User
from ..schemas.token import TokenPayload

# deprecated="auto" is used to automatically update the hashing algorithm when a better one is available
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    scopes={"admin": "Admin access", "user": "User access"},
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
  return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None, scopes: list[str] = []) -> str:
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(UTC) + expires_delta
  else:
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

  to_encode.update({"exp": expire, "scopes": scopes, "type": "access"})

  encoded_jwt = jwt.encode(
      to_encode,
      settings.SECRET_KEY,
      algorithm=settings.ALGORITHM
  )
  return encoded_jwt

async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]) -> User:
  authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": authenticate_value},
  )

  try:
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
    token_scopes = payload.get("scopes", [])
    token_payload = TokenPayload(username, scopes=token_scopes)
  except (JWTError, ValidationError):
    raise credentials_exception

