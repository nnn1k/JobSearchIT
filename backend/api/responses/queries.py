from typing import List

from sqlalchemy import and_, desc, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.core.database.models.other import ResponsesOrm
from backend.core.database.models.worker import ResumesOrm
from backend.core.database.models.employer import VacanciesOrm
from backend.core.schemas import EmployerResponseSchema, ResponseSchema, WorkerResponseSchema
from backend.core.schemas.user_schema import UserResponseSchema
from backend.core.utils.const import EMPLOYER_USER_TYPE, WORKER_USER_TYPE
from backend.core.utils.exc import (
    incorrect_user_type_exc,
    response_is_exist_exc, response_not_found_exc, resume_not_found_exc,
    user_is_not_owner_exc,
    vacancy_not_found_exc
)


async def get_vacancy_and_resume(
        session: AsyncSession,
        resume_id: int,
        vacancy_id: int,
):
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


async def get_responses_queries(
        user: UserResponseSchema,
        session: AsyncSession,
        response: bool = True
) -> List[ResponsesOrm]:
    if not user:
        raise incorrect_user_type_exc
    stmt = (
        select(ResponsesOrm)
        .options(joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.profession))
        .options(joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.worker))
        .options(joinedload(ResponsesOrm.resume).selectinload(ResumesOrm.skills))
        .options(joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.profession))
        .options(joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.company))
        .options(joinedload(ResponsesOrm.vacancy).selectinload(VacanciesOrm.skills))
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
        conditions.append(ResponsesOrm.first == WORKER_USER_TYPE)
    else:
        conditions.append(ResponsesOrm.is_employer_accepted.is_(True))
        conditions.append(ResponsesOrm.first == EMPLOYER_USER_TYPE)
    stmt = stmt.order_by(desc(ResponsesOrm.updated_at))
    stmt = stmt.where(and_(*conditions))
    result = await session.execute(stmt)
    responses = result.scalars().unique().all()
    return [ResponseSchema.model_validate(response, from_attributes=True) for response in responses]


async def send_response_queries(
        user: UserResponseSchema,
        session: AsyncSession,
        resume_id: int,
        vacancy_id: int,
):
    if not user:
        raise incorrect_user_type_exc

    resume, vacancy = await get_vacancy_and_resume(session=session, resume_id=resume_id, vacancy_id=vacancy_id)
    await check_response_is_exist(session=session, resume_id=resume_id, vacancy_id=vacancy_id)

    stmt = (
        insert(ResponsesOrm)
        .values(resume_id=resume_id, vacancy_id=vacancy_id, first=user.type)
        .returning(ResponsesOrm)
        .options(joinedload(ResponsesOrm.resume))
        .options(joinedload(ResponsesOrm.vacancy))
    )

    if user.type == WORKER_USER_TYPE:
        if resume.worker_id != user.id:
            raise user_is_not_owner_exc
        stmt = stmt.values(is_worker_accepted=True)
    elif user.type == EMPLOYER_USER_TYPE:
        if vacancy.company_id != user.company_id:
            raise user_is_not_owner_exc
        stmt = stmt.values(is_employer_accepted=True)
    else:
        raise incorrect_user_type_exc

    new_result = await session.execute(stmt)
    response = new_result.scalars().one_or_none()
    schema = ResponseSchema.model_validate(response, from_attributes=True)
    await session.commit()
    return schema


async def send_reaction_to_response(
        user: UserResponseSchema,
        session: AsyncSession,
        response_id: int,
        reaction: bool,
) -> ResponseSchema:
    response = await session.get(ResponsesOrm, response_id)
    if not response:
        raise response_not_found_exc
    resume, vacancy = await get_vacancy_and_resume(session=session, resume_id=response.resume_id,
                                                   vacancy_id=response.vacancy_id)
    if vacancy.company_id != user.company_id:
        raise user_is_not_owner_exc
    stmt = (
        update(ResponsesOrm)
        .where(ResponsesOrm.id == response_id)
        .returning(ResponsesOrm)
        .options(joinedload(ResponsesOrm.resume))
        .options(joinedload(ResponsesOrm.vacancy))
    )
    if user.type == WORKER_USER_TYPE:
        if resume.worker_id != user.id:
            raise user_is_not_owner_exc
        stmt = stmt.values(is_worker_accepted=reaction)
    elif user.type == EMPLOYER_USER_TYPE:
        if vacancy.company_id != user.company_id:
            raise user_is_not_owner_exc
        stmt = stmt.values(is_employer_accepted=reaction)
    else:
        raise incorrect_user_type_exc

    result = await session.execute(stmt)
    response = result.scalars().one_or_none()
    schema = ResponseSchema.model_validate(response, from_attributes=True)
    await session.commit()
    return schema


async def delete_response_queries(
        user: UserResponseSchema,
        session: AsyncSession,
        response_id: int
) -> None:
    response = await session.get(ResponsesOrm, response_id)
    if not response:
        raise response_not_found_exc
    resume, vacancy = await get_vacancy_and_resume(session=session, resume_id=response.resume_id,
                                                   vacancy_id=response.vacancy_id)
    if not user:
        raise incorrect_user_type_exc

    if user.type == WORKER_USER_TYPE:
        if resume.worker_id != user.id:
            raise user_is_not_owner_exc
    elif user.type == EMPLOYER_USER_TYPE:
        if vacancy.company_id != user.company_id:
            raise user_is_not_owner_exc
    else:
        raise incorrect_user_type_exc

    await session.delete(response)
    await session.commit()
