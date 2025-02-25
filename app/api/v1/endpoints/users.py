from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_authenticated_user, get_current_superuser
from app.schemas.user import UserResponse
from app.models.user import User
from typing import List, Annotated


router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_authenticated_user)]
):
  return current_user


@router.get("/users", response_model=List[UserResponse])
async def get_users(
    current_user: User = Depends(get_current_superuser)
):
  return current_user

