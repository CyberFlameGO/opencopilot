import os
from dataclasses import dataclass
from uuid import UUID
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback

import settings
from logger import api_logger
from src.domain.chat.entities import UserMessageInput
from src.repository.conversation_history_repository import ConversationHistoryRepositoryLocal

logger = api_logger.get()


@dataclass(frozen=True)
class History:
    template_with_history: str
    formatted_history: str


def add_history(
        template: str,
        chat_id: UUID,
        history_repository: ConversationHistoryRepositoryLocal,
) -> History:
    os.makedirs(settings.CONVERSATIONS_DIR, exist_ok=True)
    history = history_repository.get_prompt_history(
        chat_id, settings.PROMPT_HISTORY_INCLUDED_COUNT)
    history = history.replace("{", "{{").replace("}", "}}")
    return History(
        template_with_history=template.replace("{history}", history, 1),
        formatted_history=history,
    )


def get_system_message(prompt_directory: str = settings.PROMPTS_DIRECTORY) -> str:
    if prompt_directory != settings.PROMPTS_DIRECTORY:
        file_path = os.path.join(prompt_directory, "prompt_template.txt")
    elif settings.UNITY_COPILOT_URL:
        file_path = os.path.join(settings.PROMPTS_DIRECTORY, "prompt_template_with_unity.txt")
    else:
        file_path = os.path.join(prompt_directory, "prompt_template.txt")

    with open(file_path, "r") as f:
        return f.read()


def get_function_system_message() -> str:
    file_path = os.path.join(settings.PROMPTS_DIRECTORY, "prompt_template_unity_function.txt")

    with open(file_path, "r") as f:
        return f.read()


def get_unity_communication_prompt(domain_input: UserMessageInput,
                                   history_repository: ConversationHistoryRepositoryLocal):
    if settings.UNITY_COPILOT_URL:
        unity_history: History = add_history(
            get_function_system_message(),
            domain_input.chat_id,
            history_repository,
        )
        return unity_history.template_with_history.replace('{question}', domain_input.message, 1)

    return None

def get_context_query(query: str, history: History) -> str:
    if history.formatted_history:
        try:
            prompt = settings.RETRIEVAL_PROMPT_TEMPLATE.format(chat_history=history.formatted_history, question=query)
            logger.info(f"PROMPT {prompt}")
            with get_openai_callback() as cb:
                llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k")
                query = llm.predict(prompt)
            logger.info(cb)
        except:
            pass
    logger.info(f"RETRIEVAL QUERY {query}")
    return query
