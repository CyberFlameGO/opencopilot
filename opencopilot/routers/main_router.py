import importlib
import os
import sys

from fastapi import APIRouter

from opencopilot import settings
from opencopilot.logger import api_logger
from opencopilot.routers.routes import chat_router
from opencopilot.routers.routes import debug_router, auth_router

TAG_ROOT = "root"

router = APIRouter()
logger = api_logger.get()

routers_to_include = [
    chat_router.router,
    debug_router.router,
    auth_router.router,
]
route_titles = []
for router_to_include in routers_to_include:
    router.include_router(router_to_include)
    route_titles.append({
        "title": router_to_include.title,
        "tags": router_to_include.openapi_tags
    })


def _add_custom_endpoints():
    try:
        module_package = os.path.abspath(settings.get().COPILOT_DIRECTORY)
        module_path = "custom_endpoints"
        sys.path.append(module_package)
        custom_endpoints_module = importlib.import_module(module_path, package=module_package)
        router.include_router(custom_endpoints_module.router)
    except Exception as exc:
        logger.info(f"Failed to load custom endpoints: {exc}")


_add_custom_endpoints()
