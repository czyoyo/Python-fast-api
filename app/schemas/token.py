from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class Token(BaseModel):
  access_token: str
  token_type: str = "bearer"
  expires_in: int


class TokenPayload(BaseModel):
  sub: Optional[int] = None
  scopes: list[str] = []
  type: str = "access"
  exp: Optional[datetime] = None

