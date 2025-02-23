from datetime import datetime, UTC
from typing import Optional

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import get_password_hash, verify_password

class UserCRUD:

  def get_user(self, db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

  def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

  def get_user_by_nickname(self, db: Session, nickname: str) -> Optional[User]:
    return db.query(User).filter(User.nickname == nickname).first()


  def create_user(self, db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        nickname=user.nickname,
        hashed_password=get_password_hash(user.password),
        is_active=user.is_active,
        is_superuser=False,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )
    db.add(db_user) # db_user 를 db 에 추가
    db.commit() # db 에 반영
    db.refresh(db_user) # db_user 를 새로고침

    # 가져온 db_user 를 출력
    print("db_user 출력:", db_user)
    for key, value in db_user.__dict__.items():
      print(key, value)

    return UserResponse.model_validate(db_user.__dict__)

    # return db_user
    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        nickname=db_user.nickname,
        is_active=db_user.is_active,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at
    )

  def update(
      self, db: Session, user_id: int, user_update: UserUpdate
  ) -> Optional[User]:
    db_user = self.get_ser(db, user_id)
    if not db_user:
      return None

    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
      update_data["hashed_password"] = get_password_hash(
          update_data.pop("password")
      )

    for key, value in update_data.items():
      setattr(db_user, key, value)

    print("유저 출력:", db_user)

    db_user.updated_at = datetime.now(UTC)
    db.commit()
    db.refresh(db_user)
    return db_user

  def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
    user = self.get_user_by_email(db, email=email)
    if not user:
      return None
    if not verify_password(password, user.hashed_password):
      return None
    return user

  def is_active(self, user: User) -> bool:
    return user.is_active

  def is_superuser(self, user: User) -> bool:
    return user.is_superuser

user_crud = UserCRUD()
