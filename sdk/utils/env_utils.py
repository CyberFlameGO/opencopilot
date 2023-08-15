import os
from pathlib import Path
from urllib.parse import urljoin

from dotenv import load_dotenv

# TODO: get url from .env and fix docker-compose
FRONTEND_URL = "http://0.0.0.0:3001"


def get_backend_url():
    env_path = Path("backend") / ".env"
    load_dotenv(dotenv_path=env_path)
    port = int(os.getenv("API_PORT", 3000))
    base_url = os.getenv("API_BASE_URL", "http://0.0.0.0/")
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    return f"{base_url}:{str(port)}"


def get_backend_docs_url():
    url = get_backend_url()
    return urljoin(url, "docs")


def get_frontend_url():
    return FRONTEND_URL


def get_frontend_poll_url():
    return urljoin(get_frontend_url(), "default/favicon-16x16.png")


def get_copilot_name() -> str:
    env_path = Path("backend") / ".env"
    load_dotenv(dotenv_path=env_path)
    name = os.getenv("COPILOT_NAME", "")
    return name


def get_copilot_path():
    name = get_copilot_name()
    return os.path.join("copilots", name)
