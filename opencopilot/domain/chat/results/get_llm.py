from typing import Dict, Optional

import openai
from langchain.chat_models import ChatOpenAI

from opencopilot import settings
from opencopilot.utils.callbacks.callback_handler import CustomAsyncIteratorCallbackHandler


def execute(
        email: str = None,
        callback: CustomAsyncIteratorCallbackHandler = None,
) -> ChatOpenAI:
    if settings.get().HELICONE_API_KEY:
        openai.api_base = settings.get().HELICONE_BASE_URL
    llm = ChatOpenAI(
        temperature=0.0,
        model_name=settings.get().MODEL,
        streaming=callback is not None,
        callbacks=[callback] if callback is not None else None,
        headers=_get_headers(email)
    )
    return llm


def _get_headers(email: str = None) -> Optional[Dict]:
    if settings.get().HELICONE_API_KEY:
        if email is None:
            email = ""
        return {
            "Helicone-Auth": "Bearer " + settings.get().HELICONE_API_KEY,
            "Helicone-User-Id": email
        }
    return None
