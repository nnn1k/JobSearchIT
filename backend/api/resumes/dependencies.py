from http import HTTPStatus
from typing import Tuple, Any

from fastapi import Depends, HTTPException, status

from backend.api.resumes.repository import get_resume_repo
from backend.api.resumes.schemas import ResumeSchema, ResumeUpdateSchema
from backend.api.users.workers.dependencies import get_worker_by_token
from backend.api.users.workers.schemas import WorkerSchema
from backend.api.vacancies.schemas import VacancyAddSchema
from backend.utils.other.check_func import check_worker_can_update


async def create_resume_dependencies(
        add_resume: VacancyAddSchema,
        user: WorkerSchema = Depends(get_worker_by_token)
) -> Tuple[ResumeSchema, WorkerSchema]:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    resume_repo = get_resume_repo()
    resume = await resume_repo.add_one(**add_resume.model_dump(), worker_id=user.id)
    return resume, user

async def get_resume_dependencies(
        resume_id: int,
        user: WorkerSchema = Depends(get_worker_by_token)
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    resume_repo = get_resume_repo()
    resume = await resume_repo.get_one(id=resume_id)
    return resume, user


async def get_all_resumes_dependencies(
        user: WorkerSchema = Depends(get_worker_by_token)
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    resume_repo = get_resume_repo()
    resumes = await resume_repo.get_all(worker_id=user.id)
    return resumes, user

async def update_resume_dependencies(
        resume_id: int,
        update_resume: ResumeUpdateSchema,
        user: WorkerSchema = Depends(get_worker_by_token)
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    resume_repo = get_resume_repo()
    resume = await resume_repo.get_one(id=resume_id)
    if not check_worker_can_update(user, resume):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no rights",
        )
    new_resume = await resume_repo.update(id=resume_id, **update_resume.model_dump())
    return new_resume, user

