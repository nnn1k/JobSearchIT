from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database.models.worker import ResumesOrm, WorkersOrm
from backend.schemas.models.worker.worker_schema import WorkerResponseSchema
from backend.utils.exc import worker_not_found_exc

from backend.utils.other.time_utils import time_it_async


@time_it_async
async def get_worker_by_id_queries(worker_id: int, session: AsyncSession) -> WorkerResponseSchema:
    stmt = await session.execute(
        select(WorkersOrm)
        .filter(WorkersOrm.id == int(worker_id))
        .options(
            selectinload(WorkersOrm.resumes).selectinload(ResumesOrm.profession)
        )
    )
    worker = stmt.scalars().one_or_none()
    if not worker:
        raise worker_not_found_exc
    schema = WorkerResponseSchema.model_validate(worker, from_attributes=True)
    return schema


async def update_worker_by_id_queries(worker_id: int, session: AsyncSession, **kwargs):
    stmt = await session.execute(
        update(WorkersOrm)
        .filter_by(id=int(worker_id))
        .values(**kwargs)
        .returning(WorkersOrm)
    )
    worker = stmt.scalars().unique().one_or_none()
    if not worker:
        raise worker_not_found_exc
    await session.commit()
    return await get_worker_by_id_queries(worker_id, session)
