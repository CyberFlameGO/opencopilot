from src.domain.chat.entities import ChatContextInput
from src.domain.chat.entities import ChatContextOutput
from src.repository.conversation_user_context_repository import ConversationUserContextRepositoryLocal


def execute(
        data_input: ChatContextInput,
        repository: ConversationUserContextRepositoryLocal
) -> ChatContextOutput:
    repository.save_context(data_input)
    return ChatContextOutput(
        response="OK"
    )
