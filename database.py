from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeMeta
from typing import Generator

from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True, # 연결 확인을 위한 ping
    echo=True # SQL 쿼리 출력
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()


def get_db() -> Generator:
  """
  데이터베이스 세션을 제공하는 의존성 함수

  Yields:
      Generator: 데이터베이스 세션
  """
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

