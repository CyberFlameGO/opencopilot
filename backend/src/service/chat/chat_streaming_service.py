import json
import uuid

from src.domain.chat import on_user_message_streaming_use_case
from src.domain.chat.entities import UserMessageInput
from src.repository.conversation_history_repository import ConversationHistoryRepositoryLocal
from src.repository.conversation_logs_repository import ConversationLogsRepositoryLocal
from src.repository.conversation_user_context_repository import ConversationUserContextRepositoryLocal
from src.repository.documents.document_store import DocumentStore
from src.service.chat.entities import ChatRequest
from src.service.utils import get_uuid


async def execute(
        request: ChatRequest,
        document_store: DocumentStore,
        history_repository: ConversationHistoryRepositoryLocal,
        logs_repository: ConversationLogsRepositoryLocal,
        context_repository: ConversationUserContextRepositoryLocal
) -> str:
    chat_id = get_uuid(request.chat_id, "chat_id")
    async for chunk in on_user_message_streaming_use_case.execute(
            UserMessageInput(
                chat_id=chat_id,
                message=request.message,
                response_message_id=request.response_message_id or str(uuid.uuid4()),
                email=request.email
            ),
            document_store,
            history_repository,
            logs_repository,
            context_repository=context_repository,
    ):
        data = chunk.to_dict()
        yield f"{json.dumps(data)}\n"
