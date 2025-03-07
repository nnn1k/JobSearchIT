from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.utils.other.logger_utils import logger
from backend.utils.other.time_utils import time_it_async


@time_it_async
async def check_connection_db(session: AsyncSession):
    try:
        res = await session.execute(text('SELECT version();'))
        print(res.scalars().one_or_none())
    except Exception as e:
        logger.error(e)
