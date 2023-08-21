import datetime
import json
import os
from unittest.mock import patch
from uuid import UUID

from langchain.schema import Document

from opencopilot.domain.chat.entities import ChatContextInput
from opencopilot.repository.conversation_user_context_repository import \
    ConversationUserContextRepositoryLocal

CONTEXT_DIR = "tests/assets/contexts"
CHAT_ID = UUID("46eefec7-de17-4836-9575-75f3bee5001b")
CHAT_ID_INVALID = UUID("79f88a74-7a67-4336-b601-4cfbcaed55e1")


def setup_function():
    create_mock_context()


def teardown_function():
    delete_file()


def create_mock_context():
    data = [
        {
            "timestamp": "2023-07-10T12:27:02.541217",
            "context": "My name is George"
        }
    ]
    file_path = os.path.join(CONTEXT_DIR, str(CHAT_ID)) + ".json"
    os.makedirs(CONTEXT_DIR, exist_ok=True)
    with open(file_path, "w") as file:
        file.write(json.dumps(data, indent=4))


def delete_file():
    file_path = os.path.join(CONTEXT_DIR, str(CHAT_ID)) + ".json"
    try:
        os.remove(file_path)
    except:
        pass


def test_get_context_documents():
    repository = ConversationUserContextRepositoryLocal(CONTEXT_DIR)
    result = repository.get_context_documents(CHAT_ID, 3)
    expected = Document(
        page_content="My name is George",
        metadata={
            "timestamp": "2023-07-10T12:27:02.541217",
            "source": "user_context"
        }
    )
    assert result == [expected]


def test_get_context_documents_not_found():
    repository = ConversationUserContextRepositoryLocal(CONTEXT_DIR)
    result = repository.get_context_documents(CHAT_ID_INVALID, 1)
    assert result == []


def test_save_context():
    context_input = ChatContextInput(
        conversation_id=CHAT_ID,
        context="I use MacBook"
    )
    repository = ConversationUserContextRepositoryLocal(CONTEXT_DIR)
    mock_now = datetime.datetime(2023, 7, 10, 12, 27, 5)
    with patch("opencopilot.repository.conversation_user_context_repository.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_now
        repository.save_context(
            context_input
        )
    result = repository.get_context_documents(CHAT_ID, 3)
    expected = [
        Document(
            page_content="I use MacBook",
            metadata={
                "timestamp": "2023-07-10T12:27:05",
                "source": "user_context"
            }
        )
    ]
    assert result == expected
