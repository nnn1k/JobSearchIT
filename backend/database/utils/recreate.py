import asyncio
from backend.database.settings.database import engine, Base
from backend.database.models.worker import WorkersOrm, ResumesOrm, EducationsOrm
from backend.database.models.employer import EmployersOrm, CompaniesOrm, VacanciesOrm
from backend.database.models.other import SkillsOrm, WorkersSkillsOrm, VacanciesSkillsOrm, ResponsesOrm

async def recreate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(recreate())
