from fastapi import APIRouter, Depends

from app.schemas.user import User, UserCreate
from app.db.database import SessionLocal
from sqlalchemy.orm import Session



router = APIRouter()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


