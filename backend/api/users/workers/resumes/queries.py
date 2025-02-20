from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload

from backend.database.models.worker import ResumesOrm
from backend.database.settings.database import session_factory
from backend.schemas.models.worker.resume_schema import ResumeSchema
from backend.utils.other.logger_utils import logger


async def create_resume_queries(**kwargs):
    async with session_factory() as session:
        logger.info(f'{kwargs}')
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
            return None
        schema = ResumeSchema.model_validate(resume, from_attributes=True)
        await session.commit()
        return schema


async def get_one_resume_by_id_queries(resume_id: int, refresh: bool = False):
    if not refresh:
        ...
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
            return None
        schema = ResumeSchema.model_validate(resume, from_attributes=True)
        return schema


async def update_resume_by_id_queries(resume_id: int, worker, **kwargs):
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
            return None
        if worker.id == resume.worker.id:
            await session.commit()
            return await get_one_resume_by_id_queries(resume_id)
        return None
