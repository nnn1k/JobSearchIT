from typing import List, Sequence

from sqlalchemy import insert, select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from backend.core.database.models.employer import VacanciesOrm
from backend.core.database.models.other import ResponsesOrm
from backend.core.database.models.other.Chat import ChatsOrm
from backend.core.database.models.other.Message import MessagesOrm
from backend.core.database.models.worker import ResumesOrm
from backend.core.utils.const import WORKER_USER_TYPE, EMPLOYER_USER_TYPE
from backend.core.utils.other.type_utils import UserVar


class ChatRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_chat(self, response_id: int) -> ChatsOrm:
        stmt = (
            insert(ChatsOrm)
            .values(response_id=response_id)
            .returning(ChatsOrm)
            .options(joinedload(ChatsOrm.response))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def check_user_is_owner(self, chat_id: int, user: UserVar) -> ChatsOrm:
        stmt = (
            select(ChatsOrm)
            .join(ResponsesOrm)
            .options(selectinload(ChatsOrm.messages))
            .options(joinedload(ChatsOrm.response).joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.worker))
            .options(joinedload(ChatsOrm.response).joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.company))
        )
        if user.type == WORKER_USER_TYPE:
            stmt = stmt.join(ResumesOrm)
            stmt = stmt.where(
                and_(
                    ResumesOrm.worker_id == user.id,
                    ChatsOrm.id == chat_id,
                )
            )
        elif user.type == EMPLOYER_USER_TYPE:
            stmt = stmt.join(VacanciesOrm)
            stmt = stmt.where(
                and_(
                    VacanciesOrm.company_id == user.company_id,
                    ChatsOrm.id == chat_id
                )
            )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_chats(self, user: UserVar) -> Sequence[ChatsOrm]:
        stmt = (
            select(ChatsOrm)
            .join(ResponsesOrm)
            .options(selectinload(ChatsOrm.messages))
            .options(joinedload(ChatsOrm.response).joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.worker))
            .options(joinedload(ChatsOrm.response).joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.company))
        )
        if user.type == WORKER_USER_TYPE:
            stmt = stmt.join(ResumesOrm)
            stmt = stmt.where(and_(ResumesOrm.worker_id == user.id))
        elif user.type == EMPLOYER_USER_TYPE:
            stmt = stmt.join(VacanciesOrm)
            stmt = stmt.where(VacanciesOrm.company_id == user.company_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_chat(self, chat_id: int) -> ChatsOrm:
        stmt = (
            select(ChatsOrm)
            .filter_by(id=chat_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_messages(self, chat_id: int) -> Sequence[MessagesOrm]:
        stmt = (
            select(MessagesOrm)
            .where(and_(MessagesOrm.chat_id == chat_id))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def send_message(self, chat_id: int, message: str, sender_id: int, sender_type: str) -> MessagesOrm:
        stmt = (
            insert(MessagesOrm)
            .values(chat_id=chat_id, message=message, sender_id=sender_id, sender_type=sender_type)
            .returning(MessagesOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
