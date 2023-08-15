from typing import Optional

from starlette.requests import Request

from src.service.middleware.entitites import RequestStateKey


def set_state(request: Request, state_key: RequestStateKey, value: any):
    request.state.__setattr__(state_key.value, value)


def get_state(request: Request, state_key: RequestStateKey) -> Optional[any]:
    return getattr(request.state, state_key.value, None)
