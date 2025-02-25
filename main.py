from app.api.v1.router import api_router
from app.core.config import settings
from app.models import user
from database import engine
from app.middlewares.response import response_middleware

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.common import CommonResponse


user.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

@app.middleware("http")
async def wrap_responses(request, call_next):
    return await response_middleware(request, call_next)


# CORS 미들웨어 설정
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.BACKEND_CORS_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return "Hello, World!"


# HTTP 예외 핸들러
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """HTTP 예외를 CommonResponse 형식으로 변환"""
    return JSONResponse(
        status_code=exc.status_code,
        content=CommonResponse(
            status=exc.status_code,
            message=exc.detail,
            data=None
        ).model_dump(),
    )


# 검증 예외 핸들러
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request,
    exc: RequestValidationError):
    """검증 예외를 CommonResponse 형식으로 변환"""
    # 검증 오류 정보 추출
    errors = exc.errors()
    error_messages = []

    for error in errors:
        loc = " -> ".join(str(loc) for loc in error["loc"])
        msg = f"{loc}: {error['msg']}"
        error_messages.append(msg)

    error_msg = "; ".join(error_messages)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=CommonResponse(
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=f"입력값 검증 오류: {error_msg}",
            data=None
        ).model_dump(),
    )


# 기타 모든 예외 핸들러
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """모든 예외를 CommonResponse 형식으로 변환"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=CommonResponse(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"서버 오류: {str(exc)}",
            data=None
        ).model_dump(),
    )
