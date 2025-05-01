from typing import List

from sqlalchemy import and_, delete, desc, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.api.v1.responses.check_func import check_response_is_exist, check_user_is_not_owner, get_vacancy_and_resume
from backend.core.database.models.other.Response import ResponsesOrm
from backend.core.database.models.worker.Resume import ResumesOrm
from backend.core.database.models.employer.Vacancy import VacanciesOrm
from backend.core.schemas.models.other.response_schema import ResponseSchema
from backend.core.schemas.user_schema import UserResponseSchema
from backend.core.utils.const import EMPLOYER_USER_TYPE, WORKER_USER_TYPE


async def get_responses_queries(
        user: UserResponseSchema,
        session: AsyncSession,
        response: bool = True
) -> List[ResponseSchema]:
    stmt = (
        select(ResponsesOrm)
        .options(joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.profession))
        .options(joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.worker))
        .options(joinedload(ResponsesOrm.resume).selectinload(ResumesOrm.skills))
        .options(joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.profession))
        .options(joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.company))
        .options(joinedload(ResponsesOrm.vacancy).selectinload(VacanciesOrm.skills))
        .options(joinedload(ResponsesOrm.chat))
    )

    conditions = []

    if user.type == WORKER_USER_TYPE:
        stmt = stmt.join(ResumesOrm)
        conditions.append(ResumesOrm.worker_id == user.id)
    elif user.type == EMPLOYER_USER_TYPE:
        stmt = stmt.join(VacanciesOrm)
        conditions.append(VacanciesOrm.company_id == user.company_id)

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
) -> ResponseSchema:
    resume, vacancy = await get_vacancy_and_resume(session=session, resume_id=resume_id, vacancy_id=vacancy_id)
    await check_response_is_exist(session=session, resume_id=resume_id, vacancy_id=vacancy_id)

    stmt = (
        insert(ResponsesOrm)
        .values(resume_id=resume_id, vacancy_id=vacancy_id, first=user.type)
        .returning(ResponsesOrm)
        .options(joinedload(ResponsesOrm.resume))
        .options(joinedload(ResponsesOrm.vacancy))
    )

    check_user_is_not_owner(user=user, resume=resume, vacancy=vacancy)
    if user.type == WORKER_USER_TYPE:
        stmt = stmt.values(is_worker_accepted=True)
    elif user.type == EMPLOYER_USER_TYPE:
        stmt = stmt.values(is_employer_accepted=True)

    result = await session.execute(stmt)
    response = result.scalars().one_or_none()
    schema = ResponseSchema.model_validate(response, from_attributes=True)
    await session.commit()
    return schema


async def send_reaction_to_response(
        user: UserResponseSchema,
        session: AsyncSession,
        response_id: int,
        reaction: bool,
) -> ResponseSchema:
    resume, vacancy = await get_vacancy_and_resume(
        session=session,
        response_id=response_id,
    )

    stmt = (
        update(ResponsesOrm)
        .where(and_(ResponsesOrm.id == response_id))
        .returning(ResponsesOrm)
        .options(joinedload(ResponsesOrm.resume))
        .options(joinedload(ResponsesOrm.vacancy))
    )

    check_user_is_not_owner(user=user, resume=resume, vacancy=vacancy)

    if user.type == WORKER_USER_TYPE:
        stmt = stmt.values(is_worker_accepted=reaction)
    elif user.type == EMPLOYER_USER_TYPE:
        stmt = stmt.values(is_employer_accepted=reaction)

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
    resume, vacancy = await get_vacancy_and_resume(
        session=session,
        response_id=response_id,
    )
    check_user_is_not_owner(user=user, resume=resume, vacancy=vacancy)
    await session.execute(
        delete(ResponsesOrm)
        .where(and_(ResponsesOrm.id == response_id))
    )
    await session.commit()
