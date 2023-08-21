import json
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID

from langchain.schema import Document

from opencopilot.logger import api_logger
from opencopilot.domain.chat.entities import ChatContextInput

DEFAULT_CONTEXTS_DIR = "conversation_contexts"

logger = api_logger.get()


class ConversationUserContextRepositoryLocal:

    def __init__(self, contexts_dir: str = DEFAULT_CONTEXTS_DIR):
        self.contexts_dir = contexts_dir

    def get_context_documents(self, chat_id: UUID, count: Optional[int]) -> List[Document]:
        try:
            with open(self._get_file_path(chat_id), "r") as f:
                context = json.load(f)
            if not count or len(context) <= count:
                return self._to_documents(context)
            return self._to_documents(context[count * -1:])
        except:
            logger.error(f"Error loading conversation context, id: {str(chat_id)}")
        return []

    def get_context(self, chat_id: UUID) -> List[Dict]:
        context = []
        try:
            with open(self._get_file_path(chat_id), "r") as f:
                context = json.load(f)
        except:
            pass
        return context

    def _to_documents(self, context: List[Dict]) -> List[Document]:
        documents: List[Document] = []
        for i in context:
            documents.append(
                Document(
                    page_content=i.get("context", ""),
                    metadata={
                        "timestamp": i.get('timestamp', ''),
                        "source": "user_context"
                    }
                )
            )
        return documents

    def save_context(
            self,
            context_input: ChatContextInput
    ) -> None:
        # context = self.get_context(context_input.conversation_id)
        # context.append()
        self._write_file(
            chat_id=context_input.conversation_id,
            data=[
                {
                    "timestamp": datetime.now().isoformat(),
                    "context": context_input.context
                }
            ],
        )

    def _get_file_path(self, chat_id: UUID):
        return f"{self.contexts_dir}/{str(chat_id)}.json"

    def _write_file(self, chat_id: UUID, data):
        try:
            with open(self._get_file_path(chat_id), "w") as f:
                f.write(json.dumps(data, indent=4))
        except Exception as e:
            logger.warning(f"Failed to save context for chat {str(chat_id)}")
