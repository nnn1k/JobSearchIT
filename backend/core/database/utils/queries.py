from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.utils.logger_utils.logger_func import logger


async def check_connection_db(session: AsyncSession):
    try:
        res = await session.execute(text('SELECT version();'))
        print(res.scalars().one_or_none())
    except Exception as e:
        logger.error(e)
