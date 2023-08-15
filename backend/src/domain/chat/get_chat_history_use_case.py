from logger import api_logger
from src.repository.conversation_history_repository import ConversationHistoryRepositoryLocal
from src.service.chat.entities import ChatHistoryItem

logger = api_logger.get()


async def execute(
        chat_id: str,
        history_repository: ConversationHistoryRepositoryLocal,
) -> [ChatHistoryItem]:
    response = history_repository.get_history(
        chat_id
    )
    return_value = []
    timer = 0
    for message in response:
        prompt_timestamp = message['prompt_timestamp'] if 'prompt_timestamp' in message else timer
        response_timestamp = message['response_timestamp'] if 'response_timestamp' in message else timer + 1
        timer = max(timer, prompt_timestamp, response_timestamp) + 2
        return_value = return_value + [ChatHistoryItem(content=message['prompt'], timestamp=prompt_timestamp), ChatHistoryItem(content=message['response'], timestamp=response_timestamp)]

    return return_value
