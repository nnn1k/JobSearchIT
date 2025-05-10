from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.utils.dependencies import get_db
from backend.core.services.chats.repository import ChatRepository
from backend.core.services.chats.service import ChatService


def get_chat_repo(session: AsyncSession = Depends(get_db)):
    return ChatRepository(session=session)


def get_chat_serv(chat_repo: ChatRepository = Depends(get_chat_repo)):
    return ChatService(chat_repo=chat_repo)