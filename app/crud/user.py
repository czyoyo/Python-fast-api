from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


def get_user(db: Session, user_id: int):
  return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
  return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
  db_user = User(
      email = user.email,
      name = user.name,
      password = user.password # 비밀번호는 해싱되어 저장되어야 함
  )
  db.add(db_user) # db_user 를 db 에 추가
  db.commit() # db 에 반영
  db.refresh(db_user) # db_user 를 새로고침
  return db_user
