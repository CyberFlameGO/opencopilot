from fastapi import APIRouter
from fastapi import Body
from opencopilot.logger import api_logger
from opencopilot.service.authorization import token_service
from opencopilot.service.authorization.entities import TokenRequest
from opencopilot.service.authorization.entities import TokenResponse

TAG = "Authorization"
router = APIRouter()
router.openapi_tags = [TAG]
router.title = "Authorization router"

logger = api_logger.get()


@router.post(
    "/token",
    tags=[TAG],
    summary="Generate token.",
    response_model=TokenResponse,
)
async def evaluate(
        request: TokenRequest = Body(
            ...,
            description="Token generation input")
):
    return token_service.execute(request)
