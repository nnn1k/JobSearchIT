from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.skills.queries import update_resume_skills

from backend.api.users.workers.resumes.queries import (
    create_resume_queries,
    delete_resume_by_id_queries,
    get_one_resume_by_id_queries,
    update_resume_by_id_queries
)
from backend.api.users.workers.resumes.schemas import ResumeAddSchema, ResumeUpdateSchema
from backend.core.database.utils.dependencies import get_db
from backend.core.schemas import SkillSchema, WorkerResponseSchema
from backend.core.utils.auth_utils.check_func import check_worker_can_update
from backend.core.utils.auth_utils.user_login_dependencies import get_user_by_token, get_worker_by_token
from backend.core.utils.other.time_utils import time_it_async

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post('', summary='Создать резюме')
@time_it_async
async def add_resumes_views(
        add_resume: ResumeAddSchema,
        user: WorkerResponseSchema = Depends(get_worker_by_token),
        session: AsyncSession = Depends(get_db),
):
    skills: List[SkillSchema] = add_resume.skills
    resume = await create_resume_queries(worker_id=user.id, session=session, **add_resume.model_dump(exclude={'skills'}))
    await update_resume_skills(skills, resume.id, user)
    return {
        'status': 'ok',
        'resume': resume,
    }


@router.get('/{resume_id}', summary='Посмотреть одно резюме')
@time_it_async
async def get_one_resume_views(
        resume_id: int,
        user: WorkerResponseSchema = Depends(get_user_by_token),
        session: AsyncSession = Depends(get_db),
):
    resume = await get_one_resume_by_id_queries(resume_id=resume_id, session=session)
    can_update = check_worker_can_update(user=user, obj=resume)
    return {
        'status': 'ok',
        'resume': resume,
        'can_update': can_update,
    }


@router.put('/{resume_id}', summary='Обновить резюме')
@time_it_async
async def update_resume_views(
        resume_id: int,
        update_resume: ResumeUpdateSchema,
        user: WorkerResponseSchema = Depends(get_worker_by_token),
        session: AsyncSession = Depends(get_db),
):
    resume = await update_resume_by_id_queries(resume_id=resume_id, worker=user, session=session, **update_resume.model_dump())
    return {
        'status': 'ok',
        'resume': resume,
    }


@router.delete('/{resume_id}', summary='Удалить резюме')
async def delete_resume_views(
        resume_id: int,
        user: WorkerResponseSchema = Depends(get_worker_by_token),
        session: AsyncSession = Depends(get_db),
):
    await delete_resume_by_id_queries(resume_id=resume_id, worker=user, session=session)
    return {
        'status': 'ok',
    }
