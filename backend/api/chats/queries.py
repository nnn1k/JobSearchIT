from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from backend.core.database.models.employer import VacanciesOrm
from backend.core.database.models.other import ResponsesOrm
from backend.core.database.models.other.Chat import ChatsOrm
from backend.core.database.models.other.Message import MessagesOrm
from backend.core.database.models.worker import ResumesOrm
from backend.core.schemas.models.other.chat_schema import ChatSchema, MessageSchema
from backend.core.schemas.user_schema import UserResponseSchema
from backend.core.utils.const import EMPLOYER_USER_TYPE, WORKER_USER_TYPE
from backend.core.utils.exc import chat_not_found_exc, response_not_found_exc, user_is_not_owner_exc


def get_all_chats_on_user_stmt(user):
    stmt = (
        select(ChatsOrm)
        .join(ResponsesOrm)
        .options(selectinload(ChatsOrm.messages))
        .options(joinedload(ChatsOrm.response).joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.worker))
        .options(joinedload(ChatsOrm.response).joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.company))
    )
    if user.type == WORKER_USER_TYPE:
        stmt = stmt.join(ResumesOrm)
        stmt = stmt.where(ResumesOrm.worker_id == user.id)
    elif user.type == EMPLOYER_USER_TYPE:
        stmt = stmt.join(VacanciesOrm)
        stmt = stmt.where(VacanciesOrm.company_id == user.company_id)
    return stmt

async def check_user_is_owner_on_chat(user, chat_id, session):
    stmt = get_all_chats_on_user_stmt(user)
    stmt = stmt.where(ChatsOrm.id == chat_id)
    result = await session.execute(stmt)
    chat = result.scalars().one_or_none()
    if not chat:
        raise user_is_not_owner_exc


async def create_chat_queries(
        response_id: int,
        session: AsyncSession
):
    print('test')
    response = await session.get(ResponsesOrm, response_id)
    if not response:
        raise response_not_found_exc
    result = await session.execute(
        insert(ChatsOrm)
        .values(response_id=response_id)
        .returning(ChatsOrm)
        .options(joinedload(ChatsOrm.response))
    )
    chat = result.scalars().one_or_none()
    schema = ChatSchema.model_validate(chat, from_attributes=True)
    await session.commit()
    return schema


async def get_all_chats_on_user(
        user: UserResponseSchema,
        session: AsyncSession
) -> list[ChatSchema]:
    stmt = get_all_chats_on_user_stmt(user)
    result = await session.execute(stmt)
    chats = result.scalars().all()
    return [ChatSchema.model_validate(chat, from_attributes=True) for chat in chats]


async def get_all_messages_on_chat(
        user: UserResponseSchema,
        chat_id: int,
        session: AsyncSession
):
    chat = await session.get(ChatsOrm, chat_id)
    if not chat:
        raise chat_not_found_exc

    await check_user_is_owner_on_chat(user, chat_id, session)

    result = await session.execute(
        select(MessagesOrm)
        .where(MessagesOrm.chat_id == chat_id)
    )
    messages = result.scalars().all()

    return [MessageSchema.model_validate(message, from_attributes=True) for message in messages]


async def send_message_queries(
        user: UserResponseSchema,
        chat_id: int,
        message: str,
        session: AsyncSession
) -> None:
    await check_user_is_owner_on_chat(user, chat_id, session)
    await session.execute(
        insert(MessagesOrm)
        .values(chat_id=chat_id, message=message, sender_id=user.id, sender_type=user.type)
    )
    await session.commit()
