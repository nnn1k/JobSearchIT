from fastapi import APIRouter
from .users import worker_router, auth_router, employer_router

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(worker_router)
router.include_router(employer_router)
