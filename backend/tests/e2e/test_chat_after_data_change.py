import uuid

import settings
from scripts import chat

conversation_id = uuid.uuid4()
base_url = f"http://0.0.0.0:{settings.API_PORT}"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": settings.API_KEY
}


def _chat_conversation(message: str, expected: str):
    result = chat.conversation(
        base_url=base_url,
        conversation_id=conversation_id,
        message=message
    )
    url = f"{base_url}/v0/conversation/{conversation_id}"
    print(f"\nresult from {url}\n  {result}")
    print("  json:", result.json(), "\n")
    text = result.json()["generated_text"]
    assert expected in text


def test():
    _chat_conversation("Who is Kaspar?", "frontend engineer")
    _chat_conversation("Who is Krešimir?", "backend engineer")


if __name__ == '__main__':
    test()
