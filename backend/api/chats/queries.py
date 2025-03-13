from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.models.other import ResponsesOrm
from backend.core.database.models.other.Chat import ChatsOrm
from backend.core.database.models.other.Message import MessagesOrm
from backend.core.schemas.models.other.chat_schema import ChatSchema
from backend.core.schemas.user_schema import UserResponseSchema
from backend.core.utils.const import EMPLOYER_USER_TYPE, WORKER_USER_TYPE
from backend.core.utils.exc import response_not_found_exc


async def create_chat_queries(
        response_id: int,
        session: AsyncSession
):
    response = await session.get(ResponsesOrm, response_id)
    if not response:
        raise response_not_found_exc
    result = await session.execute(
        insert(ChatsOrm)
        .values(response_id=response_id)
        .returning(ChatsOrm)
    )
    chat = result.scalars().one_or_none()
    schema = ChatSchema.model_validate(chat, from_attributes=True)
    await session.commit()
    return schema

async def get_all_chats_queries(
        user: UserResponseSchema,
        session: AsyncSession
) -> list[ChatSchema]:
    if user.type == WORKER_USER_TYPE:
        ...
    elif user.type == EMPLOYER_USER_TYPE:
        ...

async def get_all_messages_on_chat(
    user: UserResponseSchema,
    chat_id: int,
    session: AsyncSession
):
    #TODO сделать проверку на is_owner
    result = await session.execute(
        select(MessagesOrm)
        .where(MessagesOrm.chat_id == chat_id)
    )
    messages = result.scalars().all()
    return messages

async def send_message_queries(

):
    ...
