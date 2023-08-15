from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TextWithTokens:
    text: Optional[str]
    token_count: Optional[int]


@dataclass(frozen=True)
class MessageDebugResult:
    prompt_template: Optional[TextWithTokens]
    data_sources: Optional[str]
    user_question: Optional[TextWithTokens]
    context: Optional[TextWithTokens]
    chat_history: Optional[TextWithTokens]
    full_prompt: Optional[TextWithTokens]
    # Need more data here
    llm_response: Optional[TextWithTokens]
