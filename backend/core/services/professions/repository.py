from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.models.other import ProfessionsOrm


class ProfessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_professions(self, **kwargs) -> Sequence[ProfessionsOrm]:
        stmt = (
            select(ProfessionsOrm)
            .where(**kwargs)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

