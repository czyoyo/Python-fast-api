from fastapi import APIRouter
from .endpoints import auth

api_router = APIRouter()

# prefix="/auth"로 설정된 라우터를 auth 라우터로 설정
# /auth/login, /auth/register 등의 경로로 접근 가능
# tags=["auth"]로 설정된 라우터는 Swagger UI에서 auth 그룹으로 표시됨
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
