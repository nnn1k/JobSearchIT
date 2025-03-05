from typing import List

from sqlalchemy import and_, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models.other import ResponsesOrm
from backend.database.models.worker import ResumesOrm
from backend.database.models.employer import VacanciesOrm
from backend.schemas.models.other.response_schema import ResponseSchema
from backend.schemas.user_schema import UserResponseSchema
from backend.utils.const import EMPLOYER_USER_TYPE, WORKER_USER_TYPE
from backend.utils.exc import (
    incorrect_user_type_exc,
    resume_not_found_exc,
    user_is_not_owner_exc,
    vacancy_not_found_exc
)

async def send_response_queries(
        user: UserResponseSchema,
        resume_id: int,
        vacancy_id: int,
        accept: bool,
        session: AsyncSession
) -> ResponsesOrm:
    if not user:
        raise incorrect_user_type_exc
    resume = await session.get(ResumesOrm, resume_id)
    vacancy = await session.get(VacanciesOrm, vacancy_id)
    if not resume:
        raise resume_not_found_exc
    if not vacancy:
        raise vacancy_not_found_exc

    stmt = await session.execute(
        select(ResponsesOrm)
        .filter_by(resume_id=resume_id, vacancy_id=vacancy_id)
    )
    response = stmt.scalars().one_or_none()
    if not response:
        new_stmt = (
            insert(ResponsesOrm)
            .values(resume_id=resume_id, vacancy_id=vacancy_id)
        )
    else:
        new_stmt = (
            update(ResponsesOrm)
            .where(ResponsesOrm.resume_id == resume_id, ResponsesOrm.vacancy_id == vacancy_id)
        )
    if user.type == WORKER_USER_TYPE:
        if user.id != resume.worker_id:
            raise user_is_not_owner_exc
        new_stmt = new_stmt.values(is_worker_accepted=accept)

    elif user.type == EMPLOYER_USER_TYPE:
        if user.company_id != vacancy.company_id:
            raise user_is_not_owner_exc
        new_stmt = new_stmt.values(is_employer_accepted=accept)

    new_stmt = new_stmt.returning(ResponsesOrm)
    result = await session.execute(new_stmt)
    response = result.scalars().one_or_none()
    schema = ResponseSchema.model_validate(response, from_attributes=True)
    await session.commit()
    return schema


async def get_responses_queries(
        user: UserResponseSchema,
        session: AsyncSession,
        response: bool = True
) -> List[ResponsesOrm]:
    if not user:
        raise incorrect_user_type_exc
    stmt = (
        select(ResponsesOrm)
    )
    conditions = []
    if user.type == WORKER_USER_TYPE:
        stmt = stmt.join(ResumesOrm)
        conditions.append(ResumesOrm.worker_id == user.id)

    elif user.type == EMPLOYER_USER_TYPE:
        stmt = stmt.join(VacanciesOrm)
        conditions.append(VacanciesOrm.company_id == user.company_id)
    else:
        raise incorrect_user_type_exc

    if response:
        conditions.append(ResponsesOrm.is_worker_accepted.is_(True))
    else:
        conditions.append(ResponsesOrm.is_employer_accepted.is_(True))

    stmt = stmt.where(and_(*conditions))
    result = await session.execute(stmt)
    responses = result.scalars().all()
    return [ResponseSchema.model_validate(response, from_attributes=True) for response in responses]
