from fastapi import APIRouter

from backend.api.v1.users.auth.views import router as auth_router
from backend.api.v1.users.employers.views import router as employer_router

from backend.api.v1.users.workers.views import router as profile_router


worker_router = APIRouter(prefix="/workers")

worker_router.include_router(profile_router)


router = APIRouter()
router.include_router(auth_router)
router.include_router(worker_router)
router.include_router(employer_router)
