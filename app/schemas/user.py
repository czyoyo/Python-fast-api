from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserResponse(BaseModel):
  # from_attributes=True 로 설정하면, 클래스의 속성을 통해 모델을 생성할 수 있습니다.
  model_config = ConfigDict(from_attributes=True)
  id: int
  email: EmailStr
  nickname: str
  is_active: bool
  created_at: datetime
  updated_at: datetime




class UserBase(BaseModel):
    """사용자 정보의 기본 모델"""
    email: EmailStr = Field(..., description="사용자 이메일")
    is_active: bool = True # 활성화 여부 (기본값: True)
    is_superuser: bool = False # 관리자 여부 (기본값: False)

class UserCreate(UserBase):
    """사용자 생성을 위한 모델"""
    password: str = Field(..., description="비밀번호", min_length=8) # 최소 8자리
    nickname: str = Field(..., min_length=2, max_length=20, description="닉네임") # 2 ~ 50자리


class UserUpdate(UserBase):
  """사용자 정보 업데이트를 위한 모델"""
  password: Optional[str] = None
  nickname: Optional[str] = None
  email: Optional[EmailStr] = None

class UserLogin(BaseModel):
  """사용자 로그인을 위한 모델"""
  email: EmailStr
  password: str





class UserInDBBase(UserBase):
  """DB에 저장된 사용자 정보의 기본 모델"""
  id: int
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)

# class UserResponse(UserInDBBase):
#   """API 응답용 사용자 모델"""
#   pass

class UserInDB(UserInDBBase):
  """데이터 베이스에 저장되는 사용자 모델"""
  hashed_password: str





