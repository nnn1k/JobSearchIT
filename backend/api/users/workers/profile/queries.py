from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from backend.database.models.worker import WorkersOrm
from backend.database.settings.database import session_factory
from backend.schemas.models.worker.worker_schema import WorkerResponseSchema
from backend.utils.str_const import WORKER_USER_TYPE

from backend.utils.other.celery_utils import cl_app


@cl_app.task
async def get_worker_by_id_queries(worker_id: int, refresh: bool = False):
    if not refresh:
        ...
    async with session_factory() as session:
        stmt = await session.execute(
            select(WorkersOrm)
            .options(selectinload(WorkersOrm.resumes))
            .options(selectinload(WorkersOrm.educations))
            .filter_by(id=int(worker_id))
        )
        worker = stmt.scalars().one_or_none()
        schema = WorkerResponseSchema.model_validate(worker, from_attributes=True)
        return schema

async def update_worker_by_id_queries(worker_id: int, **kwargs):
    async with session_factory() as session:
        stmt = await session.execute(
            update(WorkersOrm)
            .filter_by(id=int(worker_id))
            .values(**kwargs)
            .returning(WorkersOrm)
            .options(selectinload(WorkersOrm.resumes))
            .options(selectinload(WorkersOrm.educations))
        )
        worker = stmt.scalars().one_or_none()
        schema = WorkerResponseSchema.model_validate(worker, from_attributes=True)
        await session.commit()
        return schema
