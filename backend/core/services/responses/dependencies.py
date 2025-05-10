from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.utils.dependencies import get_db
from backend.core.services.chats.dependencies import get_chat_serv
from backend.core.services.chats.service import ChatService
from backend.core.services.responses.repository import ResponseRepository
from backend.core.services.responses.service import ResponseService
from backend.core.services.resumes.dependencies import get_resume_serv
from backend.core.services.resumes.service import ResumeService
from backend.core.services.vacancies.dependencies import get_vacancy_serv

from backend.core.services.vacancies.service import VacancyService


def get_resp_repo(session: AsyncSession = Depends(get_db)):
    return ResponseRepository(session=session)


def get_resp_serv(
        resp_repo: ResponseRepository = Depends(get_resp_repo),
        resume_serv: ResumeService = Depends(get_resume_serv),
        vacancy_serv: VacancyService = Depends(get_vacancy_serv),
        chat_serv: ChatService = Depends(get_chat_serv)
):
    return ResponseService(resp_repo=resp_repo, vacancy_serv=vacancy_serv, resume_serv=resume_serv, chat_serv=chat_serv)

