from opencopilot.src.domain.chat.entities import ChatFeedbackInput
from opencopilot.src.domain.chat.entities import ChatFeedbackOutput
from opencopilot.src.repository.conversation_history_repository import ConversationHistoryRepositoryLocal


def execute(
        data_input: ChatFeedbackInput,
        repository: ConversationHistoryRepositoryLocal
) -> ChatFeedbackOutput:
    repository.add_feedback(data_input)
    return ChatFeedbackOutput(
        response="OK"
    )
