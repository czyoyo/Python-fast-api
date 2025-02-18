from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """사용자 정보의 기본 모델"""
    email: EmailStr
    username: str

class UserCreate(UserBase):
    """사용자 생성 모델"""
    password: str

class User(UserBase):
  id: int

  class Config: # Pydantic 설정
    from_attributes = True # 클래스 속성을 필드로 사용
