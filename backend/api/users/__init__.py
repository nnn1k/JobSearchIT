from fastapi import APIRouter

from .auth import router as auth_router
from .workers.views import router as worker_router
from .employers.views import router as employer_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(worker_router)
router.include_router(employer_router)