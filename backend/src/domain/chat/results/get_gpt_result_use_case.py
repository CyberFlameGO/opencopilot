import json
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID

import aiohttp
import openai
import requests
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage
from langchain.schema import BaseMessage
from langchain.schema import Document
from langchain.schema import FunctionMessage
from langchain.schema import HumanMessage

import settings
from logger import api_logger
from src.domain.chat import get_token_count_use_case
from src.domain.chat.utils import History
from src.domain.chat.entities import LoadingMessage
from src.domain.chat.entities import UserMessageInput
from src.domain.chat.results import format_context_documents_use_case
from src.domain.chat.results import get_llm
from src.repository.conversation_history_repository import ConversationHistoryRepositoryLocal
from src.repository.conversation_logs_repository import ConversationLogsRepositoryLocal
from src.repository.conversation_user_context_repository import \
    ConversationUserContextRepositoryLocal
from src.utils.callbacks.callback_handler import CustomAsyncIteratorCallbackHandler

logger = api_logger.get()


async def execute(
        domain_input: UserMessageInput,
        system_message: str,
        context: List[Document],
        logs_repository: ConversationLogsRepositoryLocal,
        history: History,
        context_repository: Optional[ConversationUserContextRepositoryLocal] = None,
        callback: CustomAsyncIteratorCallbackHandler = None,
        unity_communication_prompt: str = None,
) -> str:
    llm = get_llm.execute(domain_input.email, callback)
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

    messages = await _get_messages(
        domain_input.message,
        prompt_text,
        domain_input,
        context_repository,
        callback,
        unity_communication_prompt
    )
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
        if token_count < (settings.get_max_token_count() * 0.75):
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

        if get_token_count_use_case.execute(prompt_text, llm) > settings.get_max_token_count():
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


async def _get_messages(
        original_query: str,
        prompt_text: str,
        domain_input: UserMessageInput,
        context_repository: Optional[ConversationUserContextRepositoryLocal],
        callback: CustomAsyncIteratorCallbackHandler = None,
        unity_communication_prompt: str = None,
) -> List[BaseMessage]:
    messages = [
        HumanMessage(content=prompt_text)
    ]
    # Use OpenAI functions to decide if we need to call Unity Copilot or get data from Local Script
    function_response = await _call_openai_function(
        domain_input,
        prompt_text,
        context_repository,
        unity_communication_prompt,
        callback
    )
    if function_response is None:
        # no functions active, return just the human message
        return messages
    extracted_message, function_name = _extract_function_message(function_response)

    if extracted_message:
        if function_name == "ask_unity_copilot":
            if callback:
                await callback.on_custom_loading_message(LoadingMessage(
                    message="Calling Unity Copilot",
                    called_copilot="unity",
                ))
            copilot_result = await _call_unity_copilot(extracted_message, domain_input.chat_id)
            if copilot_result:
                messages.append(
                    AIMessage(
                        content=f'I will call a function "{function_name}" with the message: '
                                f'"{extracted_message}"')
                )
                messages.append(FunctionMessage(content=copilot_result, name=function_name))
        elif function_name == "ask_local_copilot":
            if callback:
                await callback.on_custom_loading_message(LoadingMessage(
                    message="Calling Local Copilot",
                    called_copilot=None,
                ))
            local_script_result = _ask_local_copilot(extracted_message, domain_input.chat_id,
                                                     context_repository)
            if local_script_result:
                messages = [
                    HumanMessage(content=original_query),
                    AIMessage(
                        content=f'I will call a function "{function_name}" with the message: '
                                f'"{extracted_message}"'),
                    FunctionMessage(content=local_script_result, name=function_name)
                ]
    return messages


async def _call_openai_function(
        domain_input: UserMessageInput,
        prompt_text: str,
        context_repository: Optional[ConversationUserContextRepositoryLocal],
        unity_communication_prompt,
        callback: CustomAsyncIteratorCallbackHandler = None
):
    functions = []
    if settings.COPILOT_NAME == "unity" and context_repository is not None:
        context_documents = context_repository.get_context_documents(domain_input.chat_id, count=1)
        if len(context_documents) == 1:
            functions.append({
                "name": "ask_local_copilot",
                "description": "Use this function when user asks questions about their local "
                               "environment such as local Unity version.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "This provides information from user's local computer "
                                           "like infor about the Unity Editor. The function "
                                           "returns string not JSON."
                        }
                    },
                    "required": ["message"],
                },
            })

    if settings.UNITY_COPILOT_URL:
        if unity_communication_prompt:
            prompt_text = unity_communication_prompt
        functions.append({
            "name": "ask_unity_copilot",
            "description": "Get Unity specific information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Extracted question about Unity. The more relevant "
                                       "information provided, the better. For example, if the "
                                       "user's question is `Hello! How do I create a cube in "
                                       "Unity? Thanks!` then the message should be `How do create "
                                       "a cube in Unity?",
                    }
                },
                "required": ["message"],
            },
        })
    if len(functions) == 0:
        return None

    if callback:
        await callback.on_custom_loading_message(LoadingMessage(
            message="Syncing with copilots",
            called_copilot=None,
        ))

    response = await openai.ChatCompletion.acreate(
        model=settings.FUNCTIONS_MODEL,
        messages=[
            {"role": "system", "content": prompt_text}
        ],
        functions=functions,
        function_call="auto",
        temperature=0,
        top_p=1,
        n=1,
        stream=False,
        presence_penalty=0,
        frequency_penalty=0,
    )
    return response


def _extract_function_message(function_response):
    try:
        first_choices = function_response["choices"][0]
        function_call = first_choices["message"]["function_call"]
        function_name = function_call["name"]
        if function_name == "ask_unity_copilot":
            args = function_call["arguments"]
            if isinstance(args, str):
                args = json.loads(args)
            extracted_message = args["message"].strip()
            return extracted_message, function_name
        elif function_name == "ask_local_copilot":
            args = function_call["arguments"]
            if isinstance(args, str):
                args = json.loads(args)
            extracted_message = args["message"].strip()
            return extracted_message, function_name
    except:
        return None, None


async def _call_unity_copilot(message, uuid):
    if settings.UNITY_COPILOT_URL.endswith("/"):
        settings.UNITY_COPILOT_URL = settings.UNITY_COPILOT_URL[:-1]

    url = f"{settings.UNITY_COPILOT_URL}/v0/conversation/{uuid}"

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "inputs": message,
        "parameters": {
            "temperature": 0,
            "truncate": 0,
            "max_new_tokens": 0,
            "top_p": 0,
            "repetition_penalty": 0,
            "top_k": 0,
            "return_full_text": True
        },
        "stream": False,
        "options": {
            "id": "string",
            "response_id": "string",
            "is_retry": True,
            "use_cache": True,
            "web_search_id": "string"
        }
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps(data)) as response:
                response.raise_for_status()
                response_json = await response.json()
        message = response_json.get('generated_text', '')
        return message

    except requests.exceptions.HTTPError as errh:
        logger.error("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        logger.error("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        logger.error("Timeout Error:", errt)
    except Exception as e:
        logger.error("Something went wrong with the request:", str(e))

    return ""


def _ask_local_copilot(
        _: str,
        uuid: UUID,
        context_repository: ConversationUserContextRepositoryLocal
) -> str:
    context = context_repository.get_context_documents(uuid, count=1)
    try:
        return context[0].page_content
    except:
        return ""
