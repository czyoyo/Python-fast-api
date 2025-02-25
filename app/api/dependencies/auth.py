from typing import Annotated

from fastapi import Depends, HTTPException, status, Response
from fastapi.security import SecurityScopes

from jose import JWTError
from pydantic import ValidationError

from app.core.security import oauth2_scheme, decode_token, create_access_token
from app.schemas.token import TokenPayload
from app.services.user_service import UserService
from app.api.dependencies.services import get_user_service
from app.core.config import settings




async def verify_token(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    response: Response,
    user_service: UserService = Depends(get_user_service)
) -> TokenPayload:
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
    payload = decode_token(token)
    token_payload = TokenPayload.model_validate(payload)

    if token_payload.sub is None:
      raise credentials_exception

    # 스코프 검증
    for scope in security_scopes.scopes:
      if scope not in token_payload.scopes:
        raise scope_exception

  except (JWTError, ValidationError):
    raise credentials_exception

  user = user_service.get_user_by_id(user_id=token_payload.sub)
  if user is None:
    raise credentials_exception

  # 새로운 토큰 발급 및 헤더에 설정
  new_token = create_access_token(
    sub=token_payload.sub,
    scopes=token_payload.scopes
  )
  response.headers[settings.NEW_ACCESS_TOKEN_HEADER] = new_token

  return token_payload

# 특정 스코프에 대한 의존성 헬퍼 함수들
# - get_user_with_scopes("users:read")가 호출되어 current_user_with_scopes 함수 반환
# - current_user_with_scopes에서 SecurityScopes 객체 생성
# - verify_token_user 호출 시 이 SecurityScopes 객체가 자동으로 전달
# - ex) @router.get("/users", dependencies=[Depends(get_user_with_scopes("users:read"))])
def get_token_with_scopes(*required_scopes: str): # 하위 함수를 정의해서 반환
  """주어진 스코프에 대한 권한을 검증하는 의존성 함수를 생성합니다."""

  async def verify_scopes( # 반환된 함수를 사용 가능하게 함 (상위 함수의 인자값을 사용해서 만든 함수가 됨)
      security_scopes: SecurityScopes = SecurityScopes(scopes=required_scopes),
      token_payload: TokenPayload = Depends(verify_token)
  ) -> TokenPayload:
    return token_payload

  return verify_scopes

