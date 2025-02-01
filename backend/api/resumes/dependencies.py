from typing import Tuple

from fastapi import Depends, HTTPException, status

from backend.api.resumes.repository import get_resume_repo
from backend.api.resumes.schemas import ResumeSchema, ResumeUpdateSchema, ResumeAddSchema
from backend.api.skills.repository import update_worker_skills
from backend.api.users.auth.token_dependencies import get_user_by_token
from backend.api.users.workers.dependencies import get_worker_by_token
from backend.api.users.workers.schemas import WorkerSchema
from backend.utils.other.check_func import check_worker_can_update


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
        worker: WorkerSchema = Depends(get_worker_by_token)
) -> Tuple[ResumeSchema, WorkerSchema]:
    skills = add_resume.skills
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    resume_repo = get_resume_repo()
    resume = await resume_repo.add_one(**add_resume.model_dump(exclude='skills'), worker_id=worker.id)
    await update_worker_skills(skills, worker.id)
    return resume, worker


async def get_resume_dependencies(
        resume_id: int,
        user: WorkerSchema = Depends(get_user_by_token)
):

    resume_repo = get_resume_repo()
    resume = await resume_repo.get_one(id=resume_id)

    can_update = check_worker_can_update(user, resume)
    return resume, user, can_update


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

    can_update = check_worker_can_update(user, resumes[0])
    return resumes, user, can_update


async def update_resume_dependencies(
        resume_id: int,
        update_resume: ResumeUpdateSchema,
        worker: WorkerSchema = Depends(get_worker_by_token)
):
    resume_repo = get_resume_repo()
    resume = await resume_repo.get_one(id=resume_id)

    validate_resume_update_permissions(worker, resume)

    new_resume = await resume_repo.update_one(id=resume_id, **update_resume.model_dump())
    return new_resume, worker


async def delete_resume_dependencies(
        resume_id: int,
        worker: WorkerSchema = Depends(get_worker_by_token)
):
    resume_repo = get_resume_repo()
    resume = await resume_repo.get_one(id=resume_id)

    validate_resume_update_permissions(worker, resume)

    delete_resume = await resume_repo.soft_delete(id=resume_id, type_action='delete')
    return delete_resume, worker


