import uuid

from opencopilot.scripts import chat
from sdk.utils import env_utils


def main(message: str):
    base_url = env_utils.get_backend_url()
    chat.conversation_stream(
        base_url=base_url,
        conversation_id=uuid.uuid4(),
        message=message,
        stream=True)
