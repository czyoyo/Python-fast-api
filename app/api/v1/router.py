from fastapi import APIRouter, Depends
from .endpoints import auth, users
from ...middlewares.response import wrap_response

api_router = APIRouter(dependencies=[Depends(wrap_response())])

# prefix="/auth"로 설정된 라우터를 auth 라우터로 설정
# /auth/login, /auth/register 등의 경로로 접근 가능
# tags=["auth"]로 설정된 라우터는 Swagger UI에서 auth 그룹으로 표시됨
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/user", tags=["user"])
