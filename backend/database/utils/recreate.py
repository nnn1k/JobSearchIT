import asyncio

from backend.api.users.auth.auth_dependencies import register_user
from backend.api.users.workers.repository import get_worker_repo
from backend.api.users.workers.schemas import WorkerAuthSchema
from backend.database.settings.database import engine, Base
from backend.database.models.worker import WorkersOrm, ResumesOrm, EducationsOrm
from backend.database.models.employer import EmployersOrm, CompaniesOrm, VacanciesOrm
from backend.database.models.other import SkillsOrm, WorkersSkillsOrm, VacanciesSkillsOrm, ResponsesOrm

async def recreate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        user = await register_user(WorkerAuthSchema(email='user@gmail.com', password='user'), get_worker_repo())
        get_worker_repo().update_one(id=user.id, name='user', surname='user', patronymic='user', phone='12311111')


if __name__ == '__main__':
    asyncio.run(recreate())
