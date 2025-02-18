from dotenv import load_dotenv
import os

from pydantic.v1 import BaseSettings

load_dotenv()

class Settings(BaseSettings):
  PROJECT_NAME: str = "FastAPI" # 프로젝트 이름
  VERSION: str = "0.1.0" # 프로젝트 버전
  API_V1_STR: str = "/api/v1" # API 버전

  # JWT 설정
  SECRET_KEY: str = os.getenv("SECRET_KEY", "secret") # JWT 암호화 키, 두번째 인자는 기본값
  ALGORITHM: str = "HS256" # JWT 알고리즘
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days 만료

  # DB 설정
  DB_USER: str = os.getenv("DB_USER", "root") # DB 사용자
  DB_PASSWORD: str = os.getenv("DB_PASSWORD", "root") # DB 비밀번호
  DB_HOST: str = os.getenv("DB_HOST", "localhost") # DB 호스트
  DB_PORT: str = os.getenv("DB_PORT", "3306") # DB 포트
  DB_NAME: str = os.getenv("DB_NAME", "fastapi") # DB 이름


settings = Settings() # 설정 객체 생성

