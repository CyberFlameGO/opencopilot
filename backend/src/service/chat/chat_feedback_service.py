from src.domain.chat import chat_feedback_use_case
from src.domain.chat.entities import ChatFeedbackInput
from src.repository.conversation_history_repository import ConversationHistoryRepositoryLocal
from src.service.chat.entities import ChatFeedbackRequest
from src.service.entities import ApiResponse
from src.service.utils import get_uuid


def execute(
        conversation_id: str,
        request: ChatFeedbackRequest,
        repository: ConversationHistoryRepositoryLocal
) -> ApiResponse:
    conversation_id = get_uuid(conversation_id, "conversation_id")
    response = chat_feedback_use_case.execute(
        data_input=ChatFeedbackInput(
            conversation_id=conversation_id,
            correctness=request.correctness,
            helpfulness=request.helpfulness,
            easy_to_understand=request.easy_to_understand,
            free_form_feedback=request.free_form_feedback
        ),
        repository=repository
    )
    return ApiResponse(
        response=response.response
    )
