from fastapi import APIRouter, Depends

from app.core.auth import get_current_superuser
from app.schemas.user import UserResponse
from app.models.user import User
from typing import List

router = APIRouter()

@router.get("/users/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends()
):
  return current_user

@router.get("/users", response_model=List[UserResponse])
async def get_users(
    current_user: User = Depends(get_current_superuser)
):
  return current_user

