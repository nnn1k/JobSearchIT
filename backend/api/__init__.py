from fastapi import APIRouter
from backend.api.users import router as users_router
from backend.api.companies.views import router as company_router
from backend.api.vacancies.views import router as vacancies_router

from backend.api.skills.views import router as skills_router

router = APIRouter(prefix="/api")

router.include_router(users_router)
router.include_router(company_router)
router.include_router(vacancies_router)
router.include_router(skills_router)

