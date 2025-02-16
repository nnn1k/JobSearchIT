from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.skills.queries import update_resume_skills

from backend.api.users.workers.resumes.queries import create_resume_queries, get_one_resume_by_id_queries, \
    update_resume_by_id_queries
from backend.api.users.workers.resumes.schemas import ResumeAddSchema, ResumeUpdateSchema
from backend.schemas import SkillSchema, WorkerResponseSchema
from backend.utils.auth_utils.check_func import check_worker_can_update
from backend.utils.auth_utils.user_login_dependencies import get_user_by_token, get_worker_by_token
from backend.utils.other.time_utils import current_time

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post('/', summary='Создать резюме')
async def add_resumes_views(
        add_resume: ResumeAddSchema,
        user: WorkerResponseSchema = Depends(get_worker_by_token)
):
    skills: List[SkillSchema] = add_resume.skills
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    resume = await create_resume_queries(**add_resume.model_dump(exclude={'skills'}), worker_id=user.id)
    await update_resume_skills(skills, resume.id)
    return {
        'status': 'ok',
        'resume': resume,
        'user': user,
    }


@router.get('/{resume_id}', summary='Посмотреть одно резюме')
async def get_one_resume_views(
        resume_id: int,
        user: WorkerResponseSchema = Depends(get_user_by_token)
):
    resume = await get_one_resume_by_id_queries(resume_id)
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='resume is not exist'
        )
    can_update = check_worker_can_update(user=user, obj=resume)
    return {
        'status': 'ok',
        'resume': resume,
        'can_update': can_update,
        'user': user,
    }


@router.put('/{resume_id}', summary='Обновить резюме')
async def update_resume_views(
        resume_id: int,
        update_resume: ResumeUpdateSchema,
        user: WorkerResponseSchema = Depends(get_worker_by_token)
):
    resume = await update_resume_by_id_queries(resume_id, user, **update_resume.model_dump())
    return {
        'status': 'ok',
        'resume': resume,
        'user': user,
        'message': 'resume updated'
    }


@router.delete('/{resume_id}', summary='Удалить резюме')
async def delete_resume_views(
        resume_id: int,
        user: WorkerResponseSchema = Depends(get_worker_by_token)
):
    deleted_at = current_time()
    resume = await update_resume_by_id_queries(resume_id, user, deleted_at=deleted_at)
    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='no rights or resume not found'
        )
    return {
        'status': 'ok',
        'user': user,
        'message': 'resume deleted'
    }
