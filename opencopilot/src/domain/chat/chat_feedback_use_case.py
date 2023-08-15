from src.domain.chat.entities import ChatFeedbackInput
from src.domain.chat.entities import ChatFeedbackOutput
from src.repository.conversation_history_repository import ConversationHistoryRepositoryLocal


def execute(
        data_input: ChatFeedbackInput,
        repository: ConversationHistoryRepositoryLocal
) -> ChatFeedbackOutput:
    repository.add_feedback(data_input)
    return ChatFeedbackOutput(
        response="OK"
    )
