import logging
import os
from typing import Optional

from opencopilot import settings
from uuid import UUID
from pythonjsonlogger import jsonlogger

LOGGING_MESSAGE_FORMAT = "%(asctime)s %(name)-12s %(levelname)s %(message)s"

logger: Optional[any] = None


def get(agent_id: UUID = None):
    global logger
    if logger:
        return logger
    name = settings.APPLICATION_NAME
    file_handler = get_file_logger()
    console_handler = get_console_logger()
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    apply_default_formatter(file_handler)
    apply_default_formatter(console_handler)

    if agent_id:
        logger = logging.LoggerAdapter(logger, {'agent_id': str(agent_id)})
    return logger


def get_file_logger() -> logging.FileHandler:
    os.makedirs(os.path.dirname(settings.LOG_FILE_PATH), exist_ok=True)
    file_handler = logging.FileHandler(settings.LOG_FILE_PATH)
    file_handler.setLevel(logging.DEBUG)
    return file_handler


def get_console_logger() -> logging.StreamHandler:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    return console_handler


def apply_default_formatter(handler: logging.Handler):
    formatter = jsonlogger.JsonFormatter(LOGGING_MESSAGE_FORMAT)
    handler.setFormatter(formatter)
