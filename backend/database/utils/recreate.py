import asyncio
from sqlalchemy import text
from backend.database.settings.database import engine, Base
from backend.database.utils.models import UsersAl
async def recreate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(recreate())
