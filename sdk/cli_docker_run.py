"""
Runs backend and frontend with docker-compose

TODO:
1. Can we auto load new prompt_template after editing
2. Data reloading?
"""
from sdk import cli_validate
from sdk.utils import env_utils
from sdk.utils import print_utils
from sdk.utils import request_utils
from sdk.utils import shell_utils


def main():
    if _is_env_valid() and cli_validate.main():
        if _run_backend():
            _run_frontend()


def _is_env_valid() -> bool:
    if not shell_utils.has_docker():
        print_utils.print_red("Error: docker is not installed")
        return False
    if not shell_utils.has_docker_compose():
        print_utils.print_red("Error: docker-compose is not installed")
        return False
    if not shell_utils.is_docker_running():
        print_utils.print_red("Error: docker is not running")
        return False
    return True


def _run_backend() -> bool:
    print("(0/2) Starting backend (ETA: 5 minutes) ...")
    if shell_utils.run_backend_docker():
        backend_url = env_utils.get_backend_url()
        request_utils.poll(backend_url)
        print_utils.print_green("\n(1/2) Backend is up and running")
        print("  docs are available in:", env_utils.get_backend_docs_url())
        print("  logs are available in: backend/logs/logs-backend-service.log")
        print("  chats are available in: backend/conversations\n")
        return True
    else:
        print_utils.print_red("\nFailed to run backend, see logs under 'docker_logs'")
        return False


def _run_frontend() -> bool:
    print("(1/2) Starting frontend (ETA: 5 minutes) ...")
    if shell_utils.run_frontend_docker():
        frontend_url = env_utils.get_frontend_url()
        request_utils.poll(env_utils.get_frontend_poll_url())
        print_utils.print_green("(2/2) Frontend is up and running")
        print_utils.print_green(f"  visit chat: {frontend_url}\n")
        return True
    else:
        print_utils.print_red("\nFailed to run frontend, see logs under 'docker_logs'")
        return False


if __name__ == "__main__":
    main()
