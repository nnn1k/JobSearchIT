from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.models.employer import VacanciesOrm
from backend.core.database.models.other import ResponsesOrm
from backend.core.database.models.worker import ResumesOrm
from backend.core.utils.const import EMPLOYER_USER_TYPE, WORKER_USER_TYPE
from backend.core.utils.exc import (
    response_is_exist_exc,
    response_not_found_exc,
    resume_not_found_exc,
    user_is_not_owner_exc,
    vacancy_not_found_exc
)


async def get_vacancy_and_resume(
        session: AsyncSession,
        response_id: int = None,
        resume_id: int = None,
        vacancy_id: int = None,
):
    if response_id is not None:
        response = await session.get(ResponsesOrm, response_id)
        if not response:
            raise response_not_found_exc
        resume_id = response.resume_id
        vacancy_id = response.vacancy_id
    resume = await session.get(ResumesOrm, resume_id)
    vacancy = await session.get(VacanciesOrm, vacancy_id)
    if not resume:
        raise resume_not_found_exc
    if not vacancy:
        raise vacancy_not_found_exc
    return resume, vacancy


async def check_response_is_exist(
        session: AsyncSession,
        resume_id: int,
        vacancy_id: int,
):
    result = await session.execute(
        select(ResponsesOrm)
        .filter_by(resume_id=resume_id, vacancy_id=vacancy_id)
    )
    response = result.scalars().one_or_none()
    if response:
        raise response_is_exist_exc


def check_user_is_not_owner(user, resume, vacancy):
    if user.type == WORKER_USER_TYPE:
        if resume.worker_id != user.id:
            raise user_is_not_owner_exc
    elif user.type == EMPLOYER_USER_TYPE:
        if vacancy.company_id != user.company_id:
            raise user_is_not_owner_exc
