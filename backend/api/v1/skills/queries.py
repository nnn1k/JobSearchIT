from typing import List

from sqlalchemy import select

from backend.core.database.models.employer import VacanciesOrm
from backend.core.database.models.worker import ResumesOrm
from backend.core.schemas import WorkerSchemaRel, WorkerSchema
from backend.core.schemas import SkillSchema
from backend.core.database.models.other.VacancySkills import VacanciesSkillsOrm
from backend.core.database.models.other.Skill import SkillsOrm
from backend.core.database.models.other.ResumeSkills import ResumesSkillsOrm
from backend.core.database.database import session_factory
from backend.core.utils.exc import resume_not_found_exc, user_is_not_owner_exc, vacancy_not_found_exc


async def get_all_skills_queries(**kwargs):
    async with session_factory() as session:
        stmt = await session.execute(
            select(SkillsOrm)
            .where(**kwargs)
        )

        skills = [SkillSchema.model_validate(skill, from_attributes=True) for skill in stmt.scalars().all()]
        return skills


async def update_resume_skills(skills_list: List[SkillSchema], resume_id: int, worker: WorkerSchema):
    skills_list = [skill.id for skill in skills_list]
    async with session_factory() as session:
        stmt = await session.execute(
            select(ResumesOrm)
            .filter_by(id=resume_id)
        )
        resume = stmt.scalars().one_or_none()
        if not resume:
            raise resume_not_found_exc
        if worker.id != resume.worker_id:
            raise user_is_not_owner_exc

        result = await session.execute(select(ResumesSkillsOrm).filter_by(resume_id=resume_id))
        current_skills = result.scalars().all()

        current_skill_ids = {ws.skill_id for ws in current_skills}

        skills_to_add = set(skills_list) - current_skill_ids

        skills_to_remove = current_skill_ids - set(skills_list)
        for skill_id in skills_to_add:
            new_resume_skill = ResumesSkillsOrm(resume_id=resume_id, skill_id=skill_id)
            session.add(new_resume_skill)

        for skill_id in skills_to_remove:
            resume_skill_to_remove = await session.execute(
                select(ResumesSkillsOrm).filter_by(resume_id=resume_id, skill_id=skill_id))
            resume_skill_to_remove = resume_skill_to_remove.scalars().first()
            if resume_skill_to_remove:
                await session.delete(resume_skill_to_remove)

        await session.commit()


async def update_vacancy_skills(skills_list, vacancy_id, owner):
    skills_list = [skill.id for skill in skills_list]
    async with session_factory() as session:

        stmt = await session.execute(
            select(VacanciesOrm)
            .filter_by(id=vacancy_id)
        )
        vacancy = stmt.scalars().first()
        if not vacancy:
            raise vacancy_not_found_exc
        if owner.company_id != vacancy.company_id:
            raise user_is_not_owner_exc

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
                select(VacanciesSkillsOrm).filter_by(vacancy_id=vacancy_id, skill_id=skill_id))
            worker_skill_to_remove = worker_skill_to_remove.scalars().first()
            if worker_skill_to_remove:
                await session.delete(worker_skill_to_remove)

        await session.commit()


async def get_skills_by_resume_id(resume_id: int):
    async with session_factory() as session:
        stmt = await session.execute(
            select(ResumesOrm)
            .filter_by(id=resume_id)
        )
        resume = stmt.scalars().one_or_none()
        if not resume:
            raise resume_not_found_exc

        stmt = await session.execute(
            select(ResumesSkillsOrm)
            .filter_by(resume_id=resume_id)
        )

        resume_skills = stmt.scalars().all()

        skill_ids = [ws.skill_id for ws in resume_skills]
        resume_stmt = await session.execute(
            select(SkillsOrm)
            .filter(SkillsOrm.id.in_(skill_ids))
            .order_by(SkillsOrm.id)
        )
        available_stmt = await session.execute(
            select(SkillsOrm)
            .filter(SkillsOrm.id.notin_(skill_ids))
            .order_by(SkillsOrm.id)
        )
        resume_skills = [SkillSchema.model_validate(skill, from_attributes=True) for skill in
                         resume_stmt.scalars().all()]
        available_skills = [SkillSchema.model_validate(skill, from_attributes=True) for skill in
                            available_stmt.scalars().all()]
        return resume_skills, available_skills


async def get_skills_by_vacancy_id(vacancy_id: int):
    async with session_factory() as session:
        stmt = await session.execute(
            select(VacanciesOrm)
            .filter_by(id=vacancy_id)
        )
        vacancy = stmt.scalars().one_or_none()
        if not vacancy:
            raise vacancy_not_found_exc

        stmt = await session.execute(
            select(VacanciesSkillsOrm)
            .filter_by(vacancy_id=vacancy_id)
        )

        vacancy_skills = stmt.scalars().all()

        skill_ids = [vs.skill_id for vs in vacancy_skills]

        vacancy_stmt = await session.execute(
            select(SkillsOrm)
            .filter(SkillsOrm.id.in_(skill_ids))
            .order_by(SkillsOrm.id)
        )
        available_stmt = await session.execute(
            select(SkillsOrm)
            .filter(SkillsOrm.id.notin_(skill_ids))
            .order_by(SkillsOrm.id)
        )

        vacancy_skills = [SkillSchema.model_validate(skill, from_attributes=True) for skill in
                          vacancy_stmt.scalars().all()]
        available_skills = [SkillSchema.model_validate(skill, from_attributes=True) for skill in
                            available_stmt.scalars().all()]
        return vacancy_skills, available_skills
