from sqlalchemy import select

from backend.database.models.other import ProfessionsOrm
from backend.database.settings.database import session_factory
from backend.schemas import ProfessionSchema


async def get_professions_queries(**kwargs):
    async with session_factory() as session:
        stmt = await session.execute(
            select(ProfessionsOrm)
            .where(**kwargs)
        )
        professions = [ProfessionSchema.model_validate(pr, from_attributes=True) for pr in stmt.scalars().all()]
        return professions
