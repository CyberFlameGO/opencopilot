from fastapi import APIRouter
from fastapi import Body
from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel

router = APIRouter()
TAG = "Custom"

chain = ConversationChain(
    llm=ChatOpenAI(
        temperature=0,
        streaming=True,
    ),
    verbose=True,
)


class CustomChatRequest(BaseModel):
    message: str


class CustomChatResponse(BaseModel):
    input: str
    history: str
    response: str


@router.get(
    "/custom/chat",
    summary="Chat",
    tags=[TAG]
)
async def get_chat():
    return chain("hi")


@router.post(
    "/custom/chat",
    summary="Chat",
    tags=[TAG],
    response_model=CustomChatResponse
)
async def post_chat(
        payload: CustomChatRequest = Body(
            ...,
            description="Chat Body")
):
    return chain(payload.message)
