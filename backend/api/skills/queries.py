from typing import List

from sqlalchemy import select

from backend.schemas.models.other.skill_schema import SkillSchema
from backend.database.models.other.VacancySkills import VacanciesSkillsOrm
from backend.database.models.other.Skill import SkillsOrm
from backend.database.models.other.ResumeSkills import ResumesSkillsOrm
from backend.database.settings.database import session_factory


async def get_all_skills_queries(**kwargs):
    async with session_factory() as session:
        stmt = await session.execute(
            select(SkillsOrm)
            .where(**kwargs)
        )

        skills = [SkillSchema.model_validate(skill, from_attributes=True) for skill in stmt.scalars().all()]
        return skills


async def update_resume_skills(skills_list: List[SkillSchema], resume_id: int):
    skills_list = [skill.id for skill in skills_list]
    async with session_factory() as session:

        result = await session.execute(select(ResumesSkillsOrm).filter_by(resume_id=resume_id))
        current_skills = result.scalars().all()

        current_skill_ids = {ws.skill_id for ws in current_skills}

        skills_to_add = set(skills_list) - current_skill_ids

        skills_to_remove = current_skill_ids - set(skills_list)

        for skill_id in skills_to_add:
            new_worker_skill = ResumesSkillsOrm(resume_id=resume_id, skill_id=skill_id)
            session.add(new_worker_skill)

        for skill_id in skills_to_remove:
            worker_skill_to_remove = await session.execute(
                select(ResumesSkillsOrm).filter_by(resume_id=resume_id, skill_id=skill_id))
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


async def get_available_skills_on_resume(resume_id: int):
    async with session_factory() as session:
        stmt = (
            select(SkillsOrm)
            .outerjoin(ResumesSkillsOrm, ResumesSkillsOrm.skill_id == SkillsOrm.id)
            .filter(
                (resume_id != ResumesSkillsOrm.resume_id) |
                (ResumesSkillsOrm.resume_id.is_(None))
            )
            .order_by(SkillsOrm.id)
        )

        result = await session.execute(stmt)
        available_skills = [SkillSchema.model_validate(skill, from_attributes=True) for skill in result.scalars().all()]
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
        available_skills = [SkillSchema.model_validate(skill, from_attributes=True) for skill in result.scalars().all()]
        return available_skills


async def get_skills_by_resume_id(resume_id: int):
    async with session_factory() as session:
        stmt = select(ResumesSkillsOrm).filter_by(resume_id=resume_id)

        result = await session.execute(stmt)
        resume_skills = result.scalars().all()

        skill_ids = [ws.skill_id for ws in resume_skills]
        skills_stmt = select(SkillsOrm).filter(SkillsOrm.id.in_(skill_ids)).order_by(SkillsOrm.id)

        skills_result = await session.execute(skills_stmt)
        skills = [SkillSchema.model_validate(skill, from_attributes=True) for skill in skills_result.scalars().all()]
        return skills


async def get_skills_by_vacancy_id(vacancy_id: int):
    async with session_factory() as session:
        stmt = select(VacanciesSkillsOrm).filter_by(vacancy_id=vacancy_id)

        result = await session.execute(stmt)
        vacancy_skills = result.scalars().all()

        skill_ids = [vs.skill_id for vs in vacancy_skills]
        skills_stmt = select(SkillsOrm).filter(SkillsOrm.id.in_(skill_ids)).order_by(SkillsOrm.id)

        skills_result = await session.execute(skills_stmt)
        skills = [SkillSchema.model_validate(skill, from_attributes=True) for skill in skills_result.scalars().all()]
        return skills
