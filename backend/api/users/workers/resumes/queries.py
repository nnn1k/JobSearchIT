from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import selectinload

from backend.database.models.worker import ResumesOrm
from backend.database.settings.database import session_factory
from backend.schemas import WorkerResponseSchema
from backend.schemas.models.worker.resume_schema import ResumeSchema
from backend.utils.exc import resume_not_found_exc, user_is_not_owner_exc
from backend.utils.other.logger_utils import logger


async def create_resume_queries(**kwargs):
    async with session_factory() as session:
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


async def get_one_resume_by_id_queries(resume_id: int):
    async with session_factory() as session:
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


async def update_resume_by_id_queries(resume_id: int, worker: WorkerResponseSchema, **kwargs):
    async with session_factory() as session:
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
        return await get_one_resume_by_id_queries(resume_id)

async def delete_resume_by_id_queries(resume_id: int, worker: WorkerResponseSchema):
    async with session_factory() as session:
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

