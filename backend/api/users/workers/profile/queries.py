from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from backend.database.models.worker import WorkersOrm
from backend.database.settings.database import session_factory
from backend.schemas.models.worker.worker_schema import WorkerResponseSchema
from backend.utils.other.redis_func import cache_object, get_cached_object
from backend.utils.str_const import WORKER_USER_TYPE


async def get_worker_by_id_queries(worker_id: int):
    cache_user = await get_cached_object(obj_type=WORKER_USER_TYPE, obj_id=worker_id, schema=WorkerResponseSchema)
    if cache_user:
        return cache_user
    async with session_factory() as session:
        stmt = await session.execute(
            select(WorkersOrm)
            .options(selectinload(WorkersOrm.resumes))
            .options(selectinload(WorkersOrm.skills))
            .options(selectinload(WorkersOrm.educations))
            .filter_by(id=int(worker_id))
        )
        worker = stmt.scalars().one_or_none()
        schema = WorkerResponseSchema.model_validate(worker, from_attributes=True)
        await cache_object(schema)
        return schema

async def update_worker_by_id_queries(worker_id: int, **kwargs):
    async with session_factory() as session:
        stmt = await session.execute(
            update(WorkersOrm)
            .filter_by(id=int(worker_id))
            .values(**kwargs)
            .returning(WorkersOrm)
            .options(selectinload(WorkersOrm.resumes))
            .options(selectinload(WorkersOrm.skills))
            .options(selectinload(WorkersOrm.educations))
        )
        worker = stmt.scalars().one_or_none()
        schema = WorkerResponseSchema.model_validate(worker, from_attributes=True)
        await session.commit()
        await cache_object(schema)
        return schema
