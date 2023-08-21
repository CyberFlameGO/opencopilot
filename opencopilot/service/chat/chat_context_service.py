from opencopilot.domain.chat import chat_context_use_case
from opencopilot.domain.chat.entities import ChatContextInput
from opencopilot.repository.conversation_user_context_repository import \
    ConversationUserContextRepositoryLocal
from opencopilot.service.chat.entities import ChatContextRequest
from opencopilot.service.entities import ApiResponse
from opencopilot.service.utils import get_uuid


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
