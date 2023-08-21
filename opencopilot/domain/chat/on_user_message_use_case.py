from datetime import datetime

from opencopilot.logger import api_logger
from opencopilot.domain.chat import validate_urls_use_case
from opencopilot.domain.chat.entities import MessageModel
from opencopilot.domain.chat.entities import UserMessageInput
from opencopilot.domain.chat.results import get_gpt_result_use_case
from opencopilot.domain.chat.utils import get_system_message
from opencopilot.repository.conversation_history_repository import ConversationHistoryRepositoryLocal
from opencopilot.repository.conversation_logs_repository import ConversationLogsRepositoryLocal
from opencopilot.repository.documents.document_store import DocumentStore

logger = api_logger.get()


async def execute(
        domain_input: UserMessageInput,
        document_store: DocumentStore,
        history_repository: ConversationHistoryRepositoryLocal,
        logs_repository: ConversationLogsRepositoryLocal,
) -> MessageModel:
    system_message = get_system_message()
    context = []
    if "{context}" in system_message:
        context = document_store.find(domain_input.message)
    message_timestamp = datetime.now().timestamp()
    result = await get_gpt_result_use_case.execute(
        domain_input,
        system_message,
        context,
        logs_repository=logs_repository,
        history_repository=history_repository,
    )

    validate_urls_use_case.execute(result, domain_input.chat_id)

    response_timestamp = datetime.now().timestamp()

    history_repository.save_history(
        domain_input.message,
        result,
        message_timestamp,
        response_timestamp,
        domain_input.chat_id,
        domain_input.response_message_id,
    )
    sources = [document.metadata.get('source') for document in context]

    return MessageModel(
        chat_id=domain_input.chat_id,
        content=result,
        sources=sources
    )
