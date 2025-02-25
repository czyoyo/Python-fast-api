import secrets
from typing import Optional

from dotenv import load_dotenv
import os

from pydantic import EmailStr
from pydantic.v1 import BaseSettings

load_dotenv()

class Settings(BaseSettings):

  # 기본 설정
  API_V1_STR: str = "/api/v1" # API 버전
  PROJECT_NAME: str = "FastAPI Project" # 프로젝트 이름
  VERSION: str = "1.0.0" # 프로젝트 버전

  # JWT 설정
  SECRET_KEY: str = "my_very_secret_key_abcd_efg" # JWT 암호화 키
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
  REFRESH_TOKEN_EXPIRE_DAYS: int = 7

  # Header keys
  ACCESS_TOKEN_HEADER: str = "Authorization"
  REFRESH_TOKEN_HEADER: str = "X-Refresh-Token"


  # CORS 설정
  BACKEND_CORS_ORIGINS: list[str] = ["*"]

  # 데이터베이스 설정
  DATABASE_URL: str = "sqlite:///./sql_app.db" # SQLite 데이터베이스 파일 경로

  # 이메일 설정
  SMTP_TLS: bool = True
  SMTP_PORT: Optional[int] = None
  SMTP_HOST: Optional[str] = None
  SMTP_USER: Optional[str] = None
  SMTP_PASSWORD: Optional[str] = None
  EMAILS_FROM_EMAIL: Optional[EmailStr] = None
  EMAILS_FROM_NAME: Optional[str] = None


  class Config: # Pydantic 설정
    case_sensitive = True # 대소문자 구분 ex) name, Name 다름
    env_file = ".env" # .env 파일명 env 파일의 데이터 로드

settings = Settings()



