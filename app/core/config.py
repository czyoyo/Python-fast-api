from dotenv import load_dotenv
import os

from pydantic.v1 import BaseSettings

load_dotenv()

class Settings(BaseSettings):
  API_V1_STR: str = "/api/v1"
  PROJECT_NAME: str = "FastAPI Project"
  SECRET_KEY: str = "your-secret-key-here"  # 실제로는 환경변수로 관리
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
  SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"

  class Config: # Pydantic 설정
    case_sensitive = True # 대소문자 구분 ex) name, Name 다름

settings = Settings()



