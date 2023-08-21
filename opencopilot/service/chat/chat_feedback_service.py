from opencopilot.domain.chat import chat_feedback_use_case
from opencopilot.domain.chat.entities import ChatFeedbackInput
from opencopilot.repository.conversation_history_repository import \
    ConversationHistoryRepositoryLocal
from opencopilot.service.chat.entities import ChatFeedbackRequest
from opencopilot.service.entities import ApiResponse
from opencopilot.service.utils import get_uuid


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
