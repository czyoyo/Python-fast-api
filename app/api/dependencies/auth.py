from fastapi import Depends, HTTPException, status

from jose import jwt, JWTError
from app.core.config import settings
from app.core.security import oauth2_scheme
from app.services.user_service import UserService
from app.models.user import User
from app.api.dependencies.services import get_user_service


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> User:
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="인증할 수 없습니다",
      headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    email: str = payload.get("sub")
    if email is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception

  user = await user_service.get_user_by_email(email=email)
  if user is None:
    raise credentials_exception
  return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
  if not current_user.is_active:
    raise HTTPException(status_code=400, detail="비활성화된 사용자입니다")
  return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
  if not current_user.is_superuser:
    raise HTTPException(
        status_code=403, detail="권한이 없습니다"
    )
  return current_user
