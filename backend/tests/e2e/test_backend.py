import uuid

import requests
import settings
from scripts import chat

conversation_id = uuid.uuid4()
base_url = f"http://0.0.0.0:{settings.API_PORT}"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": settings.API_KEY
}


def _index():
    url = f"{base_url}/"
    result = requests.get(url)
    print(f"\nresult from {url}\n  {result}")
    assert result.status_code == 200
    assert result.json()


def _chat_feedback():
    url = f"{base_url}/v0/conversation/{conversation_id}/feedback"
    data = {
        "correctness": 5,
        "helpfulness": 5,
        "easy_to_understand": 5,
        "free_form_feedback": "mock feedback"
    }
    result = requests.post(url, json=data, headers=headers)
    print(f"\nresult from {url}\n  {result}")
    print("  json:", result.json(), "\n")
    assert result.json()["response"] == "OK"


def _chat_context():
    url = f"{base_url}/v0/conversation/{conversation_id}/context"
    data = {
        "context": "mock context"
    }
    result = requests.post(url, json=data, headers=headers)
    print(f"\nresult from {url}\n  {result}")
    print("  json:", result.json(), "\n")
    assert result.json()["response"] == "OK"


def _chat_conversation():
    result = chat.conversation(
        base_url=base_url,
        conversation_id=conversation_id
    )
    url = f"{base_url}/v0/conversation/{conversation_id}"
    print(f"\nresult from {url}\n  {result}")
    print("  json:", result.json(), "\n")
    assert result.json()["generated_text"]


def _chat_conversation_stream():
    result = chat.conversation_stream(
        base_url=base_url,
        conversation_id=conversation_id
    )
    url = f"{base_url}/v0/conversation_stream/{conversation_id}"
    print(f"\nresult from {url}\n  {result}")
    assert result


def _chat_history():
    url = f"{base_url}/v0/conversation/{conversation_id}/history"
    result = requests.get(url, headers=headers)
    print(f"\nresult from {url}\n  {result}")
    print("  json:", result.json(), "\n")
    assert result.json()["response"] == "OK"
    assert len(result.json()["messages"]) > 1


def main():
    _index()
    _chat_conversation()
    _chat_feedback()
    _chat_context()
    _chat_conversation_stream()
    _chat_history()


if __name__ == '__main__':
    main()
