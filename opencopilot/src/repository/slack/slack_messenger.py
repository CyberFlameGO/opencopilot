import json

import requests

import settings
from logger import api_logger

url = settings.SLACK_WEBHOOK
HEADERS = {
    "Content-type": "application/json"
}

logger = api_logger.get()


def post_error(error_type: str, error: str):
    _post_message(error_type, error)


def _post_message(error_description: str, error: str):
    if url is None or url == "":
        logger.error(f"Slack notification would be sent: {error_description} - {error}")
        return
    try:
        data = _get_data(error_description, error)
        requests.post(url, headers=HEADERS, data=json.dumps(data))
    except:
        logger.error("Failed to post error message on slack", exc_info=1)


def _get_data(error_description: str, error: str):
    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*{}*\n\nError: {}".format(
                        error_description, error)
                }
            }
        ]
    }
