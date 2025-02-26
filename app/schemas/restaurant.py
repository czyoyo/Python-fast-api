from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class RestaurantBase(BaseModel):
  """맛집 정보의 기본 모델"""
  name: str = Field(..., description="맛집 이름")
  address: str = Field(..., description="맛집 주소")
  category: Optional[str] = Field(None, description="음식 카테고리")
  latitude: Optional[float] = Field(None, description="위도")
  longitude: Optional[float] = Field(None, description="경도")
  rating: Optional[float] = Field(0.0, description="평점", ge=0, le=5)
  description: Optional[str] = Field(None, description="설명")
  phone: Optional[str] = Field(None, description="전화번호")
  image_url: Optional[str] = Field(None, description="이미지 URL")

class RestaurantCreate(RestaurantBase):
  """맛집 생성을 위한 모델"""
  pass

class RestaurantUpdate(BaseModel):
  """맛집 정보 업데이트를 위한 모델"""
  name: Optional[str] = None
  address: Optional[str] = None
  category: Optional[str] = None
  latitude: Optional[float] = None
  longitude: Optional[float] = None
  rating: Optional[float] = None
  description: Optional[str] = None
  phone: Optional[str] = None
  image_url: Optional[str] = None

class RestaurantResponse(RestaurantBase):
  """API 응답용 맛집 모델"""
  id: int
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)

class AddressSearchRequest(BaseModel):
  """주소 검색 요청 모델"""
  address: str = Field(..., description="검색할 주소")
  radius: Optional[float] = Field(1.0, description="검색 반경(km)", ge=0.1,le=10.0)
  category: Optional[str] = Field(None, description="음식 카테고리")

class RestaurantInsight(BaseModel):
  """맛집 정보와 크롤링/AI 인사이트가 포함된 모델"""
  id: int
  name: str
  address: str
  category: Optional[str] = None
  description: Optional[str] = None
  phone: Optional[str] = None
  image_url: Optional[str] = None

  # 인사이트 정보
  summary: str = ""
  recommended_menu: List[str] = []
  highlight: str = ""
  best_time_to_visit: str = ""
  tips: List[str] = []

  model_config = ConfigDict(from_attributes=True)
