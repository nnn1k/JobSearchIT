from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.core.database.models.worker import ResumesOrm
from backend.core.schemas import WorkerResponseSchema
from backend.core.schemas import ResumeSchema
from backend.core.utils.exc import resume_not_found_exc, user_is_not_owner_exc, user_have_this_profession_exc


async def create_resume_queries(session: AsyncSession, **kwargs):
    try:
        stmt = await session.execute(
            insert(ResumesOrm)
            .values(**kwargs)
            .returning(ResumesOrm)
            .options(selectinload(ResumesOrm.worker))
            .options(selectinload(ResumesOrm.skills))
            .options(selectinload(ResumesOrm.profession))
        )
        resume = stmt.scalars().one_or_none()
        if not resume:
            raise resume_not_found_exc
        schema = ResumeSchema.model_validate(resume, from_attributes=True)
        await session.commit()
        return schema
    except IntegrityError:
        raise user_have_this_profession_exc


async def get_one_resume_by_id_queries(resume_id: int, session: AsyncSession):
    stmt = await session.execute(
        select(ResumesOrm)
        .options(selectinload(ResumesOrm.worker))
        .options(selectinload(ResumesOrm.skills))
        .options(selectinload(ResumesOrm.profession))
        .where(ResumesOrm.id == int(resume_id))
    )
    resume = stmt.scalars().one_or_none()
    if not resume:
        raise resume_not_found_exc
    schema = ResumeSchema.model_validate(resume, from_attributes=True)
    return schema


async def update_resume_by_id_queries(resume_id: int, worker: WorkerResponseSchema, session: AsyncSession, **kwargs):
    stmt = await session.execute(
        update(ResumesOrm)
        .values(**kwargs)
        .filter_by(id=int(resume_id))
        .returning(ResumesOrm)
        .options(selectinload(ResumesOrm.worker))
        .options(selectinload(ResumesOrm.skills))
        .options(selectinload(ResumesOrm.profession))
    )
    resume = stmt.scalars().one_or_none()
    if not resume:
        raise resume_not_found_exc
    if not (worker.id == resume.worker.id):
        raise user_is_not_owner_exc
    await session.commit()
    return await get_one_resume_by_id_queries(resume_id, session)


async def delete_resume_by_id_queries(resume_id: int, worker: WorkerResponseSchema, session: AsyncSession):
    stmt = await session.execute(
        delete(ResumesOrm)
        .filter_by(id=int(resume_id))
        .returning(ResumesOrm)
        .options(selectinload(ResumesOrm.worker))
    )
    resume = stmt.scalars().one_or_none()
    if not resume:
        raise resume_not_found_exc
    if not (worker.id == resume.worker.id):
        raise user_is_not_owner_exc
    await session.commit()
