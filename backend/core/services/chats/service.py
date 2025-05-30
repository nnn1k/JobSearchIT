from typing import Sequence

from backend.core.schemas import ChatSchema
from backend.core.schemas.models.other.chat_schema import MessageSchema
from backend.core.services.chats.repository import ChatRepository
from backend.core.utils.exc import chat_not_found_exc, user_is_not_owner_exc
from backend.core.utils.other.type_utils import UserVar


class ChatService:
    def __init__(self, chat_repo: ChatRepository):
        self.chat_repo = chat_repo

    async def create_chat(self, response_id: int) -> ChatSchema:
        chat = self.chat_repo.create_chat(response_id=response_id)
        schema = ChatSchema.model_validate(chat)
        return schema

    async def check_user_is_owner(self, user: UserVar, chat_id: int) -> bool:
        chat = await self.chat_repo.check_user_is_owner(user=user, chat_id=chat_id)
        return bool(chat)

    async def get_all_chats(self, user: UserVar) -> Sequence[ChatSchema]:
        chats = await self.chat_repo.get_all_chats(user=user)
        return [ChatSchema.model_validate(chat) for chat in chats]

    async def get_all_messages(self, user: UserVar, chat_id: int) -> Sequence[MessageSchema]:
        chat = await self.chat_repo.get_chat(chat_id=chat_id)
        if not chat:
            raise chat_not_found_exc
        if not await self.check_user_is_owner(user=user, chat_id=chat_id):
            raise user_is_not_owner_exc
        messages = await self.chat_repo.get_all_messages(chat_id=chat_id)
        return [MessageSchema.model_validate(message) for message in messages]

    async def send_message(self, chat_id: int, message: str, user: UserVar) -> MessageSchema:

        if not await self.check_user_is_owner(user=user, chat_id=chat_id):
            raise user_is_not_owner_exc
        message = await self.chat_repo.send_message(
            chat_id=chat_id, message=message, sender_id=user.id, sender_type=user.type
        )
        schema = MessageSchema.model_validate(message)
        return schema

