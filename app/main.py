from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.models import user
from database import engine

user.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return "Hello, World!"
