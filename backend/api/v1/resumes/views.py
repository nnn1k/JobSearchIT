from collections import Counter
from typing import List

from fastapi import APIRouter, Depends, Query, BackgroundTasks

from backend.api.v1.resumes.queries import get_all_resumes_query
from backend.api.v1.skills.queries import update_resume_skills
from backend.api.v1.resumes.schemas import ResumeUpdateSchema, ResumeAddSchema
from backend.core.schemas import WorkerSchema, WorkerSchemaRel, SkillSchema
from backend.core.services.resumes.dependencies import get_resume_serv
from backend.core.services.resumes.service import ResumeService
from backend.core.utils.auth_utils.check_func import check_worker_can_update
from backend.core.utils.auth_utils.user_login_dependencies import get_user_by_token, get_worker_by_token

router = APIRouter(
    prefix="/resumes",
    tags=["resumes"],
)


@router.get('', summary='Поиск по всем резюме')
async def get_resumes_views(
    user=Depends(get_user_by_token),
    max_salary: int = Query(None, ge=0),
    profession: str = None,
    city: str = None,
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0),

):
    resumes, params = await get_all_resumes_query(
        user=user,
        max_salary=max_salary,
        profession=profession,
        city=city,
    )
    cities = Counter(resume.city for resume in resumes)
    user_type = user.type if user else None
    return {
        'params': params,
        'count': len(resumes),
        'user_type': user_type,
        'cities': cities,
        'status': 'ok',
        'resumes': resumes[(page - 1) * size:page * size],
    }

@router.post('', summary='Создать резюме')
async def add_resumes_views(
        add_resume: ResumeAddSchema,
        bg: BackgroundTasks,
        user: WorkerSchema = Depends(get_worker_by_token),
        resume_serv: ResumeService = Depends(get_resume_serv)
):
    skills: List[SkillSchema] = add_resume.skills
    resume = await resume_serv.create_resume(new_resume=add_resume, worker=user)
    bg.add_task(update_resume_skills, skills, resume.id, user)
    return {
        'resume': resume,
    }


@router.get('/{resume_id}', summary='Посмотреть одно резюме')
async def get_one_resume_views(
        resume_id: int,
        user: WorkerSchemaRel = Depends(get_user_by_token),
        resume_serv: ResumeService = Depends(get_resume_serv)
):
    resume = await resume_serv.get_resume_rel(resume_id=resume_id)
    can_update = check_worker_can_update(user=user, obj=resume)
    return {
        'resume': resume,
        'can_update': can_update,
    }


@router.put('/{resume_id}', summary='Обновить резюме')
async def update_resume_views(
        resume_id: int,
        update_resume: ResumeUpdateSchema,
        user: WorkerSchema = Depends(get_worker_by_token),
        resume_serv: ResumeService = Depends(get_resume_serv)
):
    resume = await resume_serv.update_resume(resume_id=resume_id, new_resume=update_resume, worker=user)
    return {
        'status': 'ok',
        'resume': resume,
    }


@router.delete('/{resume_id}', summary='Удалить резюме')
async def delete_resume_views(
        resume_id: int,
        user: WorkerSchema = Depends(get_worker_by_token),
        resume_serv: ResumeService = Depends(get_resume_serv)
):
    await resume_serv.delete_resume(resume_id=resume_id, worker=user)
    return {
        'status': 'ok',
    }
