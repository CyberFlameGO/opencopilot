from typing import Optional

from fastapi import APIRouter, Header
from fastapi import Body
from fastapi import Depends
from fastapi import Path
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from opencopilot.logger import api_logger
from opencopilot.authorization import validate_api_key_use_case
from opencopilot.repository.conversation_history_repository import \
    ConversationHistoryRepositoryLocal
from opencopilot.repository.conversation_logs_repository import ConversationLogsRepositoryLocal
from opencopilot.repository.conversation_user_context_repository import \
    ConversationUserContextRepositoryLocal
from opencopilot.repository.documents import document_store
from opencopilot.routers import routing_utils
from opencopilot.service import utils
from opencopilot.service.chat import chat_context_service, chat_service
from opencopilot.service.chat import chat_feedback_service, \
    chat_streaming_service, \
    chat_history_service
from opencopilot.service.chat.entities import ChatContextRequest
from opencopilot.service.chat.entities import ChatFeedbackRequest
from opencopilot.service.chat.entities import ChatHistoryRequest, ChatHistoryResponse
from opencopilot.service.chat.entities import ChatRequest
from opencopilot.service.chat.entities import ChatResponse
from opencopilot.service.entities import ApiResponse

TAG = "Chat"
router = APIRouter()
router.openapi_tags = [TAG]
router.title = "Chat router"

logger = api_logger.get()

STREAM_RESPONSE_DESCRIPTION = """
A stream of objects, delimited by newlines. Each object will be of the following form:
```
{
    "text": "some text" # the next chunk of the message from the copilot
    "error": ""         # if present, a string description of the error that occurred
}
```

For example, the message "I like to eat apples" might be streamed as follows:

```
{"text": "I like"}
{"text": " to eat"}
{"text": " apples"}
```
"""


class ConversationInput(BaseModel):
    inputs: str = Field(
        ...,
        description="Message to be answered by LLM.",
        example="How do I make a delicious lemon cheesecake?",
    )
    response_message_id: Optional[str] = Field(
        description="Optional message ID UUID, that can be used to get debug info.",
        example="e0f07564-b26b-4074-876e-d47b92ef767a",
    )

    @validator("response_message_id")
    # pylint: disable-next=no-self-argument
    def id_check(cls, v, values):
        if v:
            utils.get_uuid(v, "response_message_id")
        return v

    class Config:
        schema_extra = {
            "example": {
                "inputs": "How do I make a delicious lemon cheesecake?",
            }
        }


@router.post(
    "/conversation/{conversation_id}",
    summary="Send message to the base copilot.",
    tags=[TAG]
)
async def handle_conversation(
        email: Optional[str] = Header(default=None),
        conversation_id: str = Path(...,
                                    description="The ID of the conversation. To start a new conversation, you should pass in a random uuid (Python: `import uuid; uuid.uuid4()`). To continue a conversation, re-use the same uuid."),
        payload: ConversationInput = Body(...,
                                          description="Input and parameters for the conversation."),
        user_id: str = Depends(validate_api_key_use_case.execute)
):
    request = ChatRequest(
        chat_id=conversation_id,
        message=payload.inputs,
        response_message_id=payload.response_message_id,
        email=user_id or email
    )

    history_repository = ConversationHistoryRepositoryLocal()
    logs_repository = ConversationLogsRepositoryLocal()

    response: ChatResponse = await chat_service.execute(
        request,
        document_store.get_document_store(),
        history_repository,
        logs_repository,
    )
    return routing_utils.to_json_response({
        "generated_text": response.message,
        "sources": response.sources
    })


@router.post(
    "/conversation/{conversation_id}/feedback",
    tags=[TAG],
    summary="Send feedback to a conversation.",
    response_model=ApiResponse,
)
async def post_feedback(
        conversation_id: str = Path(..., description="The ID of the conversation."),
        payload: ChatFeedbackRequest = Body(..., description="User feedback")
):
    history_repository = ConversationHistoryRepositoryLocal()
    response = chat_feedback_service.execute(
        conversation_id=conversation_id,
        request=payload,
        repository=history_repository)
    return routing_utils.to_json_response(response.dict())


@router.post(
    "/conversation/{conversation_id}/context",
    tags=[TAG],
    summary="Send additional context for conversation.",
    response_model=ApiResponse,
)
async def post_context(
        conversation_id: str = Path(..., description="The ID of the conversation."),
        payload: ChatContextRequest = Body(..., description="User context")
):
    context_repository = ConversationUserContextRepositoryLocal()
    response = chat_context_service.execute(
        conversation_id=conversation_id,
        request=payload,
        repository=context_repository)
    return routing_utils.to_json_response(response.dict())


@router.post(
    "/conversation_stream/{conversation_id}",
    summary="Send message to the base copilot and get the response as a stream.",
    response_description=STREAM_RESPONSE_DESCRIPTION,
    tags=[TAG]
)
async def handle_conversation_streaming(
        email: Optional[str] = Header(default=None),
        conversation_id: str = Path(..., description="The ID of the conversation."),
        payload: ConversationInput = Body(...,
                                          description="Input and parameters for the conversation."),
        user_id: str = Depends(validate_api_key_use_case.execute)
):
    request = ChatRequest(
        chat_id=conversation_id,
        message=payload.inputs,
        response_message_id=payload.response_message_id,
        email=user_id or email
    )

    history_repository = ConversationHistoryRepositoryLocal()
    logs_repository = ConversationLogsRepositoryLocal()

    headers = {
        'X-Content-Type-Options': 'nosniff',
        'Connection': 'keep-alive',
    }
    return StreamingResponse(
        chat_streaming_service.execute(
            request,
            document_store.get_document_store(),
            history_repository,
            logs_repository,
        ),
        headers=headers,
        media_type="text/event-stream"
    )


@router.get(
    "/conversation/{conversation_id}/history",
    summary="Retrieve conversation history.",
    tags=[TAG]
)
async def handle_get_conversation_history(
        conversation_id: str = Path(..., description="The ID of the conversation."),
):
    request = ChatHistoryRequest(
        chat_id=conversation_id,
    )

    history_repository = ConversationHistoryRepositoryLocal()

    response: ChatHistoryResponse = await chat_history_service.execute(
        request,
        history_repository,
    )
    return response
