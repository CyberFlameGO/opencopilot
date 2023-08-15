import json
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID

import settings
from logger import api_logger
from src.domain.chat.entities import ChatFeedbackInput

DEFAULT_CONVERSATIONS_DIR = "conversations"

logger = api_logger.get()

QUESTION_KEY = f"{settings.PROMPT_QUESTION_KEY}"
RESPONSE_KEY = f"{settings.PROMPT_ANSWER_KEY}"


class ConversationHistoryRepositoryLocal:

    def __init__(
            self,
            conversations_dir: str = DEFAULT_CONVERSATIONS_DIR,
            question_key: str = QUESTION_KEY,
            response_key: str = RESPONSE_KEY,
    ):
        self.conversations_dir = conversations_dir
        self.question_key = question_key
        self.response_key = response_key

    def get_prompt_history(self, chat_id: UUID, count: Optional[int]) -> str:
        try:
            with open(self._get_file_path(chat_id), "r") as f:
                history = json.load(f)
            if not count or len(history) <= count:
                return self._to_string(history)
            return self._to_string(history[count * -1:])
        except:
            logger.debug(f"Cannot load conversation history, id: {str(chat_id)}")
        return ""

    def get_history(self, chat_id: UUID) -> List[Dict]:
        history = []
        try:
            with open(self._get_file_path(chat_id), "r") as f:
                history = json.load(f)
        except:
            pass
        return history

    def _to_string(self, history: List[Dict]) -> str:
        formatted: str = ""
        for i in history:
            formatted += f"{self.question_key}: {i.get('prompt', '')}\n"
            formatted += f"{self.response_key}: {i.get('response', '')}\n"
        return formatted

    def save_history(
            self,
            message: str,
            result: str,
            prompt_timestamp: float,
            response_timestamp: float,
            chat_id: UUID,
            response_message_id: str,
    ) -> None:
        history = self.get_history(chat_id)
        history.append({
            "prompt": message,
            "response": result.strip(),
            "prompt_timestamp": prompt_timestamp,
            "response_timestamp": response_timestamp,
            "response_message_id": response_message_id,
        })
        self._write_file(chat_id, history)

    def add_feedback(
            self,
            chat_feedback: ChatFeedbackInput
    ) -> None:
        history = self.get_history(chat_feedback.conversation_id)
        history[-1]["user_feedback"] = {
            "correctness": chat_feedback.correctness,
            "helpfulness": chat_feedback.helpfulness,
            "easy_to_understand": chat_feedback.easy_to_understand,
            "free_form_feedback": chat_feedback.free_form_feedback,
        }
        self._write_file(chat_feedback.conversation_id, history)

    def _get_file_path(self, chat_id: UUID):
        return f"{self.conversations_dir}/{str(chat_id)}.json"

    def _write_file(self, chat_id: UUID, data):
        try:
            with open(self._get_file_path(chat_id), "w") as f:
                f.write(json.dumps(data, indent=4))
        except Exception as e:
            logger.warning(f"Failed to save history for chat {str(chat_id)}")
