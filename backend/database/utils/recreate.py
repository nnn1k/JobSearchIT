from backend.database.settings.database import engine, Base
from backend.database.models import UsersAl

async def recreate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

import asyncio

asyncio.run(recreate())