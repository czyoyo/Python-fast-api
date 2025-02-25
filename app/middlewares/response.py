from app.schemas.common import CommonResponse
from typing import Any

def wrap_response():
  """모든 API 응답을 감싸는 데코레이터"""
  async def dependency(response: Any) -> CommonResponse:
    # 이미 CommonResponse로 감싸진 응답은 그대로 반환
    if isinstance(response, CommonResponse):
      return response

    # 그렇지 않으면 래핑
    return CommonResponse(
        status=200,
        message="Success",
        data=response
    )

  return dependency

