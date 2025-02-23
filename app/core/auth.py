from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes

from jose import JWTError
from pydantic import ValidationError

from app.core.security import oauth2_scheme, decode_token
from app.services.user_service import UserService
from app.models.user import User
from app.api.dependencies.services import get_user_service


async def verify_token_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserService = Depends(get_user_service)
) -> User:
  """토큰을 검증하고 해당하는 사용자를 반환합니다."""
  authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="인증할 수 없습니다",
      headers={"WWW-Authenticate": authenticate_value},
  )
  scope_exception = HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="해당 작업에 대한 권한이 없습니다",
      headers={"WWW-Authenticate": authenticate_value},
  )

  try:
    token_payload = decode_token(token)
    if token_payload.sub is None:
      raise credentials_exception

    # 스코프 검증
    for scope in security_scopes.scopes:
      if scope not in token_payload.scopes:
        raise scope_exception

  except (JWTError, ValidationError):
    raise credentials_exception

  user = await user_service.get_user_by_id(user_id=token_payload.sub)
  if user is None:
    raise credentials_exception

  return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(verify_token_user)]
) -> User:
  """현재 활성화된 사용자인지 확인합니다."""
  if not current_user.is_active:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="비활성화된 사용자입니다"
    )
  return current_user


async def get_current_superuser(
    current_user: Annotated[User, Depends(verify_token_user)]
) -> User:
  """현재 사용자가 관리자 권한을 가지고 있는지 확인합니다."""
  if not current_user.is_superuser:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="관리자 권한이 필요합니다"
    )
  return current_user


# 특정 스코프에 대한 의존성 헬퍼 함수들
def get_user_with_scopes(*required_scopes: str):
  """주어진 스코프에 대한 권한을 가진 사용자를 반환하는 의존성 함수를 생성합니다."""

  async def current_user_with_scopes(
      security_scopes: SecurityScopes = SecurityScopes(scopes=required_scopes),
      user: User = Depends(verify_token_user)
  ) -> User:
    return user

  return current_user_with_scopes

async def get_current_authenticated_user(
    user: Annotated[User, Depends(verify_token_user)]
) -> User:
  """기본 인증된 사용자를 반환합니다."""
  return user
