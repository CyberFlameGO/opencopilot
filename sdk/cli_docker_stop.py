from sdk.utils import print_utils
from sdk.utils import shell_utils


def main():
    if _is_env_valid():
        if shell_utils.stop_frontend_docker():
            print_utils.print_green("Frontend stopped")
        else:
            print_utils.print_red("Failed to stop frontend")
        if shell_utils.stop_backend_docker():
            print_utils.print_green("Backend stopped")
        else:
            print_utils.print_red("Failed to stop backend")


def _is_env_valid() -> bool:
    if not shell_utils.has_docker():
        print_utils.print_red("Error: docker is not installed")
        return False
    if not shell_utils.has_docker_compose():
        print_utils.print_red("Error: docker-compose is not installed")
        return False
    return True
