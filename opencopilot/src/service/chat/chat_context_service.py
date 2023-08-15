from opencopilot.src.domain.chat import chat_context_use_case
from opencopilot.src.domain.chat.entities import ChatContextInput
from opencopilot.src.service.chat.entities import ChatContextRequest
from opencopilot.src.repository.conversation_user_context_repository import ConversationUserContextRepositoryLocal
from opencopilot.src.service.entities import ApiResponse
from opencopilot.src.service.utils import get_uuid


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
