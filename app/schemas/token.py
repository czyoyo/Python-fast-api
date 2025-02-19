from typing import Optional

from pydantic import BaseModel

class Token(BaseModel):
  access_token: str
  token_type: str = "bearer"
  expires_in: int


class TokenPayload(BaseModel):
  sub: Optional[int] = None
  scopes: list[str] = []

