from typing import Tuple, List

from fastapi import Depends, HTTPException, status

from backend.api.users.workers.resumes.queries import create_resume_queries, get_one_resume_by_id_queries, \
    update_resume_by_id_queries
from backend.api.users.workers.resumes.schemas import ResumeUpdateSchema, ResumeAddSchema
from backend.schemas import ResumeSchema
from backend.api.skills.queries import update_worker_skills
from backend.schemas.skill_schema import SkillSchema
from backend.utils.auth_utils.token_dependencies import get_user_by_token
from backend.api.users.workers.profile.dependencies import get_worker_by_token
from backend.schemas import WorkerResponseSchema
from backend.utils.auth_utils.check_func import check_worker_can_update
from backend.utils.other.time_utils import current_time


def validate_resume_update_permissions(worker, resume):
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    if not check_worker_can_update(worker, resume):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no rights",
        )


async def create_resume_dependencies(
        add_resume: ResumeAddSchema,
        worker: WorkerResponseSchema = Depends(get_worker_by_token)
) -> Tuple['ResumeSchema', WorkerResponseSchema]:
    skills: List[SkillSchema] = add_resume.skills
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    resume = await create_resume_queries(**add_resume.model_dump(exclude={'skills'}), worker_id=worker.id)
    await update_worker_skills(skills, worker.id)
    return resume, worker


async def get_one_resume_dependencies(
        resume_id: int,
        user: WorkerResponseSchema = Depends(get_user_by_token)
):
    resume = await get_one_resume_by_id_queries(resume_id)
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='resume is not exist'
        )
    can_update = check_worker_can_update(resume, user)
    return resume, user, can_update


async def update_resume_dependencies(
        resume_id: int,
        update_resume: ResumeUpdateSchema,
        worker: WorkerResponseSchema = Depends(get_worker_by_token)
):
    resume = await update_resume_by_id_queries(resume_id, worker, **update_resume.model_dump())
    return resume, worker


async def delete_resume_dependencies(
        resume_id: int,
        worker: WorkerResponseSchema = Depends(get_worker_by_token)
):
    deleted_at = current_time()
    resume = await update_resume_by_id_queries(resume_id, worker, deleted_at=deleted_at)
    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='no rights or resume not found'
        )
    return resume, worker
