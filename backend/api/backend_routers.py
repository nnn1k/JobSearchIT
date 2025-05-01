from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.test_router import test_router
from backend.api.v1.users.router import router as users_router
from backend.api.v1.companies.views import router as company_router
from backend.api.v1.vacancies.views import router as vacancies_router
from backend.api.v1.professions.views import router as professions_router
from backend.api.v1.resumes.views import router as resumes_router
from backend.api.v1.chats.views import router as chats_router

from backend.api.v1.skills.views import router as skills_router
from backend.api.v1.responses.views import router as responses_router

router = APIRouter(prefix="/api")

router.include_router(users_router)
router.include_router(company_router)
router.include_router(vacancies_router)
router.include_router(skills_router)
router.include_router(professions_router)
router.include_router(resumes_router)
router.include_router(responses_router)
router.include_router(chats_router)

router.include_router(test_router)
