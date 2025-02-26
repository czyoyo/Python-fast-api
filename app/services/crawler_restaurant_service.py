import httpx
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
import random
from datetime import datetime

from app.core.config import settings
from app.schemas.restaurant import RestaurantResponse

load_dotenv() # Load .env file

class NaverRestaurantService:
  """네이버 API를 사용하며 맛집을 검색하는 서비스"""

  def __init__(self):
    self.naver_client_id = os.getenv("NAVER_CLIENT_ID")
    self.naver_client_secret = os.getenv("NAVER_CLIENT_SECRET")

    if not self.naver_client_id or not self.naver_client_secret:
      print("경고: 네이버 API 키가 설정되지 않았습니다.")


  async def search_restaurants_by_address(self, address: str, radius: float = 1.0, category: Optional[str] = None, display: int = 5) -> List[RestaurantResponse]:
    """
            네이버 지역 검색 API를 사용하여 주소 근처의 맛집을 검색합니다.

            Args:
                address: 검색할 주소
                radius: 검색 반경(km) - 네이버 API에서는 직접 지원하지 않음
                category: 음식 카테고리
                display: 검색 결과 개수 (최대 5)

            Returns:
                RestaurantResponse 목록
    """

    # 검색어 구성 f 는 문자열 포매팅을 의미
    query = f"{address} "
    if category:
      query += f"{category} "
    query += "맛집"

