from fastapi import APIRouter
from .users import router as users_router
from .companies import company_router
from .vacancies import vacancies_router

router = APIRouter(prefix="/api")

router.include_router(users_router)
router.include_router(company_router)
router.include_router(vacancies_router)
