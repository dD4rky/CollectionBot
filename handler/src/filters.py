from aiogram.filters import Filter
from aiogram.types import Message


class ChatTypeFilter(Filter):
    def __init__(self, chat_type: str | list[str]) -> None:
        self.chat_type = chat_type
    async def __call__(self, msg: Message) -> bool:
        return msg.chat.type in self.chat_type

class MessageTypeFilter(Filter):
    def __init__(self, message_type: str) -> None:
        self.message_type = message_type
    async def __call__(self, msg: Message) -> bool:
        return msg.content_type == self.message_type
        
