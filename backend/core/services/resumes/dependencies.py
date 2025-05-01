from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.utils.dependencies import get_db
from backend.core.services.resumes.repository import ResumeRepository
from backend.core.services.resumes.service import ResumeService


def get_resume_repo(session: AsyncSession = Depends(get_db)) -> ResumeRepository:
    return ResumeRepository(session)


def get_resume_serv(resume_repo: ResumeRepository = Depends(get_resume_repo)) -> ResumeService:
    return ResumeService(resume_repo)
