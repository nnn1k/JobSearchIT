from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload

from backend.database.models.worker import ResumesOrm, WorkersOrm
from backend.database.settings.database import session_factory
from backend.schemas.resume_schema import ResumeSchema


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
    async with session_factory() as session:
        stmt = await session.execute(
            select(ResumesOrm)
            .options(selectinload(ResumesOrm.worker).selectinload(WorkersOrm.skills))
            .where(ResumesOrm.id == int(resume_id))
        )
        resume = stmt.scalars().one_or_none()
        return ResumeSchema.model_validate(resume, from_attributes=True)


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
            return schema
        return None
