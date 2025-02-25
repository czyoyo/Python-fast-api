from fastapi import Request
from fastapi.responses import JSONResponse
import json

from app.schemas.common import CommonResponse


async def response_middleware(request: Request, call_next):
  """모든 API 응답을 CommonResponse 형식으로 변환하는 미들웨어"""

  # 특정 경로는 제외 (API 문서 등)
  exclude_paths = ["/docs", "/openapi.json", "/redoc"]
  if any(request.url.path.startswith(path) for path in exclude_paths):
    return await call_next(request)

  # API 경로가 아니면 제외
  # if not request.url.path.startswith("/api"):
  #   return await call_next(request)

  # 요청 처리
  response = await call_next(request)

  # 성공 응답(200)만 처리
  if response.status_code != 200:
    return response

  # JSON 응답만 처리
  content_type = response.headers.get("content-type", "")
  if "application/json" not in content_type:
    return response

  # 응답 본문 읽기
  body = b""
  async for chunk in response.body_iterator:
    body += chunk

  if not body:
    return response

  try:
    # 응답 데이터 파싱
    data = json.loads(body)

    # 이미 CommonResponse 형식인지 확인
    if (
        isinstance(data, dict) and
        "status" in data and
        "message" in data and
        "data" in data
    ):
      # 이미 올바른 형식이면 그대로 반환
      return JSONResponse(
          content=data,
          status_code=response.status_code
      )

    # CommonResponse로 래핑
    wrapped_data = CommonResponse(
        status=response.status_code,
        message="Success",
        data=data
    ).model_dump()

    # 새 응답 생성
    return JSONResponse(
        content=wrapped_data,
        status_code=response.status_code
    )

  except Exception as e:
    # 오류 발생 시 원본 응답 그대로 반환
    print(f"응답 미들웨어 오류: {str(e)}")
    return response
