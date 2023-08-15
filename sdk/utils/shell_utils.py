import os
import subprocess
import time
from dataclasses import dataclass

BACKEND_DIR = "backend"
BACKEND_DOCKER_COMPOSE = "docker-compose.yml"

FRONTEND_DIR = "frontend"
FRONTEND_DOCKER_COMPOSE = "docker-compose.yml"


@dataclass(frozen=True)
class ShellOutput:
    return_code: int
    logs: str


def execute_command(bash_command: str) -> ShellOutput:
    log_path = _get_log_path()
    with open(log_path, "w", encoding="utf-8") as output:
        output.write(f"Executing command: '{bash_command}'\n")
        proc = subprocess.run(
            bash_command,
            shell=True,  # pass single string to shell, let it handle.
            stdout=output,
            stderr=output
        )
        return_code = proc.returncode
    while not output.closed:
        time.sleep(0.1)
    with open(log_path, "r", encoding="utf-8") as file:
        return ShellOutput(
            return_code=return_code,
            logs=file.read()
        )


def run_backend_docker() -> bool:
    """
    Returns True if successful, False otherwise
    """
    bash_command = f"cd {BACKEND_DIR} && " \
                   f"docker compose -f {BACKEND_DOCKER_COMPOSE} up --build --remove-orphans -d"
    output = execute_command(bash_command)
    return output.return_code == 0


def run_frontend_docker() -> bool:
    """
    Returns True if successful, False otherwise
    """
    bash_command = f"cd {FRONTEND_DIR} && " \
                   f"docker compose -f {FRONTEND_DOCKER_COMPOSE} up --build --remove-orphans -d"
    output = execute_command(bash_command)
    return output.return_code == 0


def stop_backend_docker() -> bool:
    """
    Returns True if successful, False otherwise
    """
    bash_command = f"cd {BACKEND_DIR} && " \
                   f"docker compose -f {BACKEND_DOCKER_COMPOSE} down"
    output = execute_command(bash_command)
    return output.return_code == 0


def stop_frontend_docker() -> bool:
    """
    Returns True if successful, False otherwise
    """
    bash_command = f"cd {FRONTEND_DIR} && " \
                   f"docker compose -f {FRONTEND_DOCKER_COMPOSE} down"
    output = execute_command(bash_command)
    return output.return_code == 0


def has_docker() -> bool:
    output = execute_command(bash_command="docker --version")
    if output.return_code == 0 and "Docker version" in output.logs:
        return True
    return False


def has_docker_compose() -> bool:
    output = execute_command(bash_command="docker compose --version")
    if output.return_code == 0 and "Docker Compose version" in output.logs:
        return True
    return False


def is_docker_running() -> bool:
    output = execute_command(bash_command="docker info")
    if output.return_code == 0:
        return True
    return False


def _create_docker_log_file():
    log_location, log_name = "docker_logs", "output.log"
    log_path = os.path.join(os.getcwd(), log_location, log_name)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    assert os.path.isdir(os.path.dirname(log_path))
    if not os.path.isfile(log_path):
        with open(log_path, "w") as file:
            file.write("")

    return log_location, log_name, log_path


def _get_log_path():
    log_location, log_name, log_path = _create_docker_log_file()
    return log_path
