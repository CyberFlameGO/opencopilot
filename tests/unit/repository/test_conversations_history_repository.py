import json
import os
from uuid import UUID

from opencopilot.domain.chat.entities import ChatFeedbackInput
from opencopilot.repository.conversation_history_repository import ConversationHistoryRepositoryLocal

CONVERSATIONS_DIR = "tests/assets/conversations"
CHAT_ID = UUID("79f88a74-7a67-4336-b601-4cfbcaed55ef")
CHAT_ID_INVALID = UUID("79f88a74-7a67-4336-b601-4cfbcaed55e1")


def setup_function():
    create_mock_conversation()


def teardown_function():
    create_mock_conversation()


def create_mock_conversation():
    data = [
        {"prompt": "Prompt", "response": "Response"},
        {"prompt": "Prompt2", "response": "Response2"}
    ]
    file_path = os.path.join(CONVERSATIONS_DIR, str(CHAT_ID)) + ".json"
    os.makedirs(CONVERSATIONS_DIR, exist_ok=True)
    with open(file_path, "w") as file:
        file.write(json.dumps(data, indent=4))


def test_get_prompt_history_default():
    repository = ConversationHistoryRepositoryLocal(
        CONVERSATIONS_DIR,
        question_key="MockQues",
        response_key="MockRes")
    result = repository.get_prompt_history(CHAT_ID, 4)
    print("result:", result)
    expected = "MockQues: Prompt\nMockRes: Response\n" \
               "MockQues: Prompt2\nMockRes: Response2\n"
    assert result == expected


def test_get_prompt_history_count_1():
    repository = ConversationHistoryRepositoryLocal(
        CONVERSATIONS_DIR,
        question_key="MockQues",
        response_key="MockRes")
    result = repository.get_prompt_history(CHAT_ID, 1)
    expected = "MockQues: Prompt2\nMockRes: Response2\n"
    assert result == expected


def test_get_prompt_history_not_found():
    repository = ConversationHistoryRepositoryLocal(CONVERSATIONS_DIR)
    result = repository.get_prompt_history(CHAT_ID_INVALID, 1)
    assert result == ""


def test_get_history():
    repository = ConversationHistoryRepositoryLocal(CONVERSATIONS_DIR)
    result = repository.get_history(CHAT_ID)
    expected = [
        {"prompt": "Prompt", "response": "Response"},
        {"prompt": "Prompt2", "response": "Response2"}
    ]
    assert result == expected


def test_get_history_not_found():
    repository = ConversationHistoryRepositoryLocal(CONVERSATIONS_DIR)
    result = repository.get_history(CHAT_ID_INVALID)
    expected = []
    assert result == expected


def test_save_history():
    repository = ConversationHistoryRepositoryLocal(CONVERSATIONS_DIR)
    repository.save_history(
        message="Prompt3",
        result="Response3",
        chat_id=CHAT_ID,
        prompt_timestamp=123,
        response_timestamp=124,
        response_message_id="mock_id"
    )
    result = repository.get_history(CHAT_ID)
    expected = [
        {"prompt": "Prompt", "response": "Response"},
        {"prompt": "Prompt2", "response": "Response2"},
        {"prompt": "Prompt3", "response": "Response3", "prompt_timestamp": 123,
         "response_timestamp": 124, "response_message_id": "mock_id"}
    ]
    assert result == expected


def test_add_feedback():
    repository = ConversationHistoryRepositoryLocal(CONVERSATIONS_DIR)
    repository.add_feedback(
        chat_feedback=ChatFeedbackInput(
            conversation_id=CHAT_ID,
            correctness=1,
            helpfulness=2,
            easy_to_understand=3,
            free_form_feedback="mock free form"
        )
    )
    result = repository.get_history(CHAT_ID)
    expected = [
        {"prompt": "Prompt", "response": "Response"},
        {"prompt": "Prompt2", "response": "Response2", "user_feedback": {
            "correctness": 1,
            "helpfulness": 2,
            "easy_to_understand": 3,
            "free_form_feedback": "mock free form"
        }}
    ]
    assert result == expected
