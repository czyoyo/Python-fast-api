from typing import Optional, Generic, TypeVar

from pydantic import BaseModel

# Generic Type
T = TypeVar("T")

class CommonResponse(BaseModel, Generic[T]):
  status: int = 200
  message: str = "Success"
  data: Optional[T] = None

# 사용 예시를 위한 토큰 응답 모델
class TokenData(BaseModel):
  access_token: str
  refresh_token: str
