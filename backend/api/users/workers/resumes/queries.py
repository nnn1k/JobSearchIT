from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload

from backend.database.models.worker import ResumesOrm, WorkersOrm
from backend.database.settings.database import session_factory
from backend.schemas.models.worker.resume_schema import ResumeSchema
from backend.modules.redis.redis_utils import cache_object, get_cached_object
from backend.utils.str_const import RESUME_TYPE

from backend.utils.other.celery_utils import cl_app


async def create_resume_queries(**kwargs):
    async with session_factory() as session:
        stmt = await session.execute(
            insert(ResumesOrm)
            .values(**kwargs)
            .returning(ResumesOrm)
            .options(selectinload(ResumesOrm.worker))
            .options(selectinload(ResumesOrm.skills))
        )
        resume = stmt.scalars().one_or_none()
        if not resume:
            return None
        schema = ResumeSchema.model_validate(resume, from_attributes=True)
        await session.commit()
        return schema


@cl_app.task
async def get_one_resume_by_id_queries(resume_id: int, refresh: bool = False):
    if not refresh:
        cache_resume = await get_cached_object(obj_type=RESUME_TYPE, obj_id=resume_id, schema=ResumeSchema)
        if cache_resume:
            return cache_resume
    async with session_factory() as session:
        stmt = await session.execute(
            select(ResumesOrm)
            .options(selectinload(ResumesOrm.worker))
            .options(selectinload(ResumesOrm.skills))
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
