from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload

from backend.database.models.worker import ResumesOrm, WorkersOrm
from backend.database.settings.database import session_factory
from backend.schemas.models.worker.resume_schema import ResumeSchema
from backend.utils.other.redis_func import cache_object, get_cached_object
from backend.utils.str_const import RESUME_TYPE


async def create_resume_queries(**kwargs):
    async with session_factory() as session:
        stmt = await session.execute(
            insert(ResumesOrm)
            .values(**kwargs)
            .returning(ResumesOrm)
            .options(selectinload(ResumesOrm.worker).selectinload(WorkersOrm.skills))
        )
        resume = stmt.scalars().one_or_none()
        if not resume:
            return None
        schema = ResumeSchema.model_validate(resume, from_attributes=True)
        await session.commit()
        return schema


async def get_one_resume_by_id_queries(resume_id: int):
    cache_resume = await get_cached_object(obj_type=RESUME_TYPE, obj_id=resume_id, schema=ResumeSchema)
    if cache_resume:
        return cache_resume
    async with session_factory() as session:
        stmt = await session.execute(
            select(ResumesOrm)
            .options(selectinload(ResumesOrm.worker).selectinload(WorkersOrm.skills))
            .where(ResumesOrm.id == int(resume_id))
        )
        resume = stmt.scalars().one_or_none()
        schema = ResumeSchema.model_validate(resume, from_attributes=True)
        await cache_object(schema)
        return schema


async def update_resume_by_id_queries(resume_id: int, worker, **kwargs):
    async with session_factory() as session:
        stmt = await session.execute(
            update(ResumesOrm)
            .values(**kwargs)
            .filter_by(id=int(resume_id))
            .returning(ResumesOrm)
            .options(selectinload(ResumesOrm.worker).selectinload(WorkersOrm.skills))
        )
        resume = stmt.scalars().one_or_none()
        if not resume:
            return None
        schema = ResumeSchema.model_validate(resume, from_attributes=True)
        if worker.id == resume.worker.id:
            await session.commit()
            await cache_object(schema)
            return schema
        return None
