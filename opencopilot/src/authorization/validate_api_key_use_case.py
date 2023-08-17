from typing import Optional

import jwt
from fastapi import Security
from fastapi.security import APIKeyHeader

from opencopilot import settings
from opencopilot.src.service import error_responses

API_KEY_NAME = "Authorization"
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def execute(api_key_header: str = Security(API_KEY_HEADER)) -> Optional[str]:
    if not settings.get().AUTH_TYPE:
        return None

    if not api_key_header:
        raise error_responses.AuthorizationMissingAPIError
    if api_key_header.startswith("Bearer "):
        return await _validate_jwt(api_key_header[7:])
    if api_key_header != settings.get().API_KEY:
        raise error_responses.AuthorizationMissingAPIError


async def _validate_jwt(payload: str) -> str:
    try:
        payload = jwt.decode(payload, settings.get().JWT_CLIENT_SECRET, algorithms=['HS256'])
        return payload.get("sub")
    except:
        raise error_responses.AuthorizationMissingAPIError
