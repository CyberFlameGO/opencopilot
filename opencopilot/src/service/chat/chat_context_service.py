from src.domain.chat import chat_context_use_case
from src.domain.chat.entities import ChatContextInput
from src.service.chat.entities import ChatContextRequest
from src.repository.conversation_user_context_repository import ConversationUserContextRepositoryLocal
from src.service.entities import ApiResponse
from src.service.utils import get_uuid


def execute(
        conversation_id: str,
        request: ChatContextRequest,
        repository: ConversationUserContextRepositoryLocal
) -> ApiResponse:
    conversation_id = get_uuid(conversation_id, "conversation_id")
    response = chat_context_use_case.execute(
        data_input=ChatContextInput(
            conversation_id=conversation_id,
            context=request.context,
        ),
        repository=repository
    )
    return ApiResponse(
        response=response.response
    )
