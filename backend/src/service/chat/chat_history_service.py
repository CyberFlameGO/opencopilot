from src.domain.chat import get_chat_history_use_case
from src.repository.conversation_history_repository import ConversationHistoryRepositoryLocal
from src.service.chat.entities import ChatHistoryRequest
from src.service.chat.entities import ChatHistoryResponse
from src.service.utils import get_uuid


async def execute(
        request: ChatHistoryRequest,
        history_repository: ConversationHistoryRepositoryLocal,
) -> ChatHistoryResponse:
    chat_id = get_uuid(request.chat_id, "chat_id")
    messages = await get_chat_history_use_case.execute(
        chat_id,
        history_repository,
    )
    return ChatHistoryResponse(
        response="OK",
        chat_id=str(chat_id),
        messages=messages,
    )
