from fastapi import APIRouter, Depends

from app.api.dependencies.auth import verify_token
from app.api.dependencies.services import get_user_service
from app.schemas.token import TokenPayload
from app.schemas.user import UserResponse

from app.services.user_service import UserService


router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    token_payload: TokenPayload = Depends(verify_token),
    user_service: UserService = Depends(get_user_service)
)-> UserResponse:
  return user_service.get_user_info(token_payload.sub)


