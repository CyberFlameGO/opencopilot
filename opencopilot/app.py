from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from opencopilot import settings
from opencopilot.src.repository.documents import document_store
from opencopilot.src.routers import main_router
from opencopilot.src.routers import routing_utils
from opencopilot.src.service.exception_handlers.exception_handlers import custom_exception_handler
from opencopilot.src.service.middleware.main_middleware import MainMiddleware
from opencopilot.src.service.middleware.request_enrichment_middleware import RequestEnrichmentMiddleware

app = FastAPI()

app.include_router(
    main_router.router,
    prefix="/v0"
)

API_TITLE = "API"
API_DESCRIPTION = "API"
API_VERSION = "0.1"


class ApiInfo(BaseModel):
    title: str
    description: str
    version: str

    class Config:
        schema_extra = {
            "example": {
                "title": API_TITLE,
                "description": API_DESCRIPTION,
                "version": API_VERSION
            }
        }


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API",
        version="1.0.0",
        description="API version 1.0.0",
        routes=app.routes,
        servers=_get_servers()
    )
    openapi_schema["info"]["contact"] = {
        "name": "",
        "email": ""
    }
    openapi_schema["info"]["x-logo"] = {
        "url": ""
    }
    openapi_schema["x-readme"] = {
        "samples-languages": [
            "curl",
            "node",
            "javascript",
            "python"
        ]
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def _get_servers():
    servers = []
    if settings.is_production():
        pass
    else:
        base_url = settings.API_BASE_URL
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        servers.append({"url": f"{base_url}:{settings.API_PORT}"})
    return servers


app.openapi = custom_openapi

# order of middleware matters! first middleware called is the last one added
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(MainMiddleware)
app.add_middleware(RequestEnrichmentMiddleware)

# exception handlers run AFTER the middlewares!
# Handles API error responses
app.add_exception_handler(Exception, custom_exception_handler)

# Overrides FastAPI error responses, eg: authorization, not found
# app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
# Overrides default Pydantic request validation errors
# app.add_exception_handler(RequestValidationError, validation_exception_handler)

document_store.init_document_store()


def get_api_info() -> ApiInfo:
    return ApiInfo(
        title=API_VERSION,
        description=API_DESCRIPTION,
        version=API_VERSION
    )


@app.get(
    "/",
    summary="Returns API information",
    description="Returns API information",
    response_description="API information with title, description and version.",
    response_model=ApiInfo,
    include_in_schema=not settings.is_production())
def root():
    return routing_utils.to_json_response(get_api_info().dict())
