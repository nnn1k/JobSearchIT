from typing import List

from sqlalchemy import select

from backend.api.skills.schemas import SkillSchema, SkillsResponseSchema
from backend.database.models.other import SkillsOrm, VacanciesSkillsOrm, WorkersSkillsOrm
from backend.database.settings.database import session_factory
from backend.database.utils.repository import AlchemyRepository


class SkillsRepository(AlchemyRepository):
    db_model = SkillsOrm
    schema = SkillSchema


def get_skills_repo():
    return SkillsRepository()


async def get_all_skills(**kwargs):
    skills_repo = get_skills_repo()
    skills = await skills_repo.get_all(**kwargs)
    return skills


async def update_worker_skills(skills_list: List[SkillsResponseSchema], worker_id: int):
    skills_list = [skill.id for skill in skills_list]
    async with session_factory() as session:

        result = await session.execute(select(WorkersSkillsOrm).filter_by(worker_id=worker_id))
        current_skills = result.scalars().all()

        current_skill_ids = {ws.skill_id for ws in current_skills}

        skills_to_add = set(skills_list) - current_skill_ids

        skills_to_remove = current_skill_ids - set(skills_list)

        for skill_id in skills_to_add:
            new_worker_skill = WorkersSkillsOrm(worker_id=worker_id, skill_id=skill_id)
            session.add(new_worker_skill)

        for skill_id in skills_to_remove:
            worker_skill_to_remove = await session.execute(
                select(WorkersSkillsOrm).filter_by(worker_id=worker_id, skill_id=skill_id))
            worker_skill_to_remove = worker_skill_to_remove.scalars().first()
            if worker_skill_to_remove:
                await session.delete(worker_skill_to_remove)

        await session.commit()


async def update_vacancy_skills(skills_list, vacancy_id):
    skills_list = [skill.id for skill in skills_list]
    async with session_factory() as session:

        result = await session.execute(select(VacanciesSkillsOrm).filter_by(vacancy_id=vacancy_id))
        current_skills = result.scalars().all()

        current_skill_ids = {vs.skill_id for vs in current_skills}

        skills_to_add = set(skills_list) - current_skill_ids

        skills_to_remove = current_skill_ids - set(skills_list)

        for skill_id in skills_to_add:
            new_worker_skill = VacanciesSkillsOrm(vacancy_id=vacancy_id, skill_id=skill_id)
            session.add(new_worker_skill)

        for skill_id in skills_to_remove:
            worker_skill_to_remove = await session.execute(
                select(VacanciesSkillsOrm).filter_by(worker_id=vacancy_id, skill_id=skill_id))
            worker_skill_to_remove = worker_skill_to_remove.scalars().first()
            if worker_skill_to_remove:
                await session.delete(worker_skill_to_remove)

        await session.commit()


async def get_available_skills_on_worker(worker_id: int):
    async with session_factory() as session:
        stmt = (
            select(SkillsOrm)
            .outerjoin(WorkersSkillsOrm, WorkersSkillsOrm.skill_id == SkillsOrm.id)
            .filter(
                (worker_id != WorkersSkillsOrm.worker_id) |
                (WorkersSkillsOrm.worker_id.is_(None))
            )
            .order_by(SkillsOrm.id)
        )

        result = await session.execute(stmt)
        available_skills = result.scalars().all()
        return available_skills


async def get_available_skills_on_vacancy(vacancy_id: int):
    async with session_factory() as session:
        stmt = (
            select(SkillsOrm)
            .outerjoin(VacanciesSkillsOrm, VacanciesSkillsOrm.skill_id == SkillsOrm.id)
            .filter((vacancy_id != VacanciesSkillsOrm.vacancy_id) | (VacanciesSkillsOrm.vacancy_id.is_(None)))
            .order_by(SkillsOrm.id)
        )

        result = await session.execute(stmt)
        available_skills = result.scalars().all()
        return available_skills


async def get_skills_by_worker_id(worker_id: int):
    async with session_factory() as session:
        stmt = select(WorkersSkillsOrm).filter_by(worker_id=worker_id)

        result = await session.execute(stmt)
        worker_skills = result.scalars().all()

        skill_ids = [ws.skill_id for ws in worker_skills]
        skills_stmt = select(SkillsOrm).filter(SkillsOrm.id.in_(skill_ids)).order_by(SkillsOrm.id)

        skills_result = await session.execute(skills_stmt)
        skills = skills_result.scalars().all()
        return skills


async def get_skills_by_vacancy_id(vacancy_id: int):
    async with session_factory() as session:
        stmt = select(VacanciesSkillsOrm).filter_by(vacancy_id=vacancy_id)

        result = await session.execute(stmt)
        vacancy_skills = result.scalars().all()

        skill_ids = [vs.skill_id for vs in vacancy_skills]
        skills_stmt = select(SkillsOrm).filter(SkillsOrm.id.in_(skill_ids)).order_by(SkillsOrm.id)

        skills_result = await session.execute(skills_stmt)
        skills = skills_result.scalars().all()
        return skills
