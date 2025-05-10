from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.utils.dependencies import get_db
from backend.core.database.utils.queries import check_connection_db
from backend.core.utils.redis_utils.redis_obj_utils import check_redis_connection, clear_redis

test_router = APIRouter(prefix='/test', tags=['test'])


@test_router.get('/redis_connect_test')
async def redis_connect_test():
    await check_redis_connection()
    return {'status': 'ok'}


@test_router.get('/redis_clear')
async def redis_clear():
    await clear_redis()
    return {'status': 'ok'}


@test_router.get('/db_connect')
async def db_connect(
        session: AsyncSession = Depends(get_db)
):
    await check_connection_db(session)
    return {'status': 'ok'}
