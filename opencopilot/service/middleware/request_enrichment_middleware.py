import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from opencopilot.logger import api_logger
from opencopilot.service.middleware import util
from opencopilot.service.middleware.entitites import RequestStateKey

logger = api_logger.get()


class RequestEnrichmentMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: ASGIApp,
    ) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.time()
        request_id = uuid.uuid4()

        request_source = request.headers.get('source')
        request_origin = request.headers.get('origin')
        request_user_agent = request.headers.get('user-agent')
        ip_address = request.headers.get("x-forwarded-for", "").split(",")[0]

        util.set_state(request, RequestStateKey.REQUEST_ID, request_id)
        util.set_state(request, RequestStateKey.REQUEST_SOURCE, request_source)
        util.set_state(request, RequestStateKey.REQUEST_ORIGIN, request_origin)
        util.set_state(request, RequestStateKey.REQUEST_USER_AGENT, request_user_agent)
        util.set_state(request, RequestStateKey.IP_ADDRESS, ip_address)

        time_elapsed = time.time() - start
        if time_elapsed > 1:
            logger.debug(f"Middleware Enrichment before request time: {time_elapsed}")

        return await call_next(request)
