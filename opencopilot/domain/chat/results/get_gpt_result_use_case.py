from typing import List
from typing import Tuple

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.schema import HumanMessage

from opencopilot import settings
from opencopilot.logger import api_logger
from opencopilot.domain.chat import get_token_count_use_case
from opencopilot.domain.chat import utils
from opencopilot.domain.chat.entities import UserMessageInput
from opencopilot.domain.chat.results import format_context_documents_use_case
from opencopilot.domain.chat.results import get_llm
from opencopilot.repository.conversation_history_repository import \
    ConversationHistoryRepositoryLocal
from opencopilot.repository.conversation_logs_repository import ConversationLogsRepositoryLocal
from opencopilot.utils.callbacks.callback_handler import CustomAsyncIteratorCallbackHandler

logger = api_logger.get()


async def execute(
        domain_input: UserMessageInput,
        system_message: str,
        context: List[Document],
        logs_repository: ConversationLogsRepositoryLocal,
        history_repository: ConversationHistoryRepositoryLocal,
        callback: CustomAsyncIteratorCallbackHandler = None,
) -> str:
    llm = get_llm.execute(domain_input.email, callback)

    history = utils.add_history(
        system_message,
        domain_input.chat_id,
        history_repository,
    )
    logs_repository.log_history(
        domain_input.chat_id,
        domain_input.message,
        history.formatted_history,
        domain_input.response_message_id,
        token_count=get_token_count_use_case.execute(
            history.formatted_history, llm),
    )

    prompt_text = _get_prompt_text(
        domain_input,
        history.template_with_history,
        context,
        llm,
        logs_repository,
    )

    logs_repository.log_prompt_text(
        domain_input.chat_id,
        domain_input.message,
        prompt_text,
        domain_input.response_message_id,
        token_count=get_token_count_use_case.execute(prompt_text, llm),
    )
    logs_repository.log_prompt_template(
        domain_input.chat_id,
        domain_input.message,
        system_message,
        domain_input.response_message_id,
        token_count=get_token_count_use_case.execute(
            system_message,
            llm,
            is_use_cache=True
        ),
    )

    messages = [
        HumanMessage(content=prompt_text)
    ]
    result_message = await llm.agenerate([messages])
    result = result_message.generations[0][0].text
    return result


def _get_context(
        documents: List[Document],
        llm: ChatOpenAI,
) -> Tuple[str, int]:
    while len(documents):
        context = format_context_documents_use_case.execute(documents)
        token_count = get_token_count_use_case.execute(context, llm)
        # Naive solution: leaving 25% for non-context in prompt
        if token_count < (settings.get().get_max_token_count() * 0.75):
            return context, len(documents)
        documents = documents[:-1]
    return "", 0


def _get_prompt_text(
        domain_input: UserMessageInput,
        template_with_history: str,
        context_documents: List[Document],
        llm: ChatOpenAI,
        logs_repository: ConversationLogsRepositoryLocal,
) -> str:
    # Almost duplicated with get_local_llm_result_use_case._get_prompt_text
    context, context_documents_count = _get_context(context_documents, llm)
    prompt_text = ""
    if "{context}" in template_with_history:
        prompt = PromptTemplate(
            template=template_with_history,
            input_variables=["context", "question"])

        prompt_text = prompt.format_prompt(**{
            "context": context,
            "question": domain_input.message
        }).to_string()

        if get_token_count_use_case.execute(prompt_text, llm) > settings.get().get_max_token_count():
            prompt_text = ""
        logs_repository.log_context(
            domain_input.chat_id,
            domain_input.message,
            context_documents[0: context_documents_count],
            domain_input.response_message_id,
            token_count=get_token_count_use_case.execute(context, llm),
        )
    if not prompt_text:
        prompt = PromptTemplate(
            template=template_with_history,
            input_variables=["context", "question"])
        prompt_text = prompt.format_prompt(**{
            "context": "",
            "question": domain_input.message
        }).to_string()
    return prompt_text
