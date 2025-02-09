from fastapi import APIRouter

from backend.api.users.auth.views import router as auth_router
from .employers.views import router as employer_router

from backend.api.users.workers.profile.views import router as profile_router
from backend.api.users.workers.resumes.views import router as resumes_router

worker_router = APIRouter(prefix="/workers")

worker_router.include_router(profile_router)
worker_router.include_router(resumes_router)


router = APIRouter()
router.include_router(auth_router)
router.include_router(worker_router)
router.include_router(employer_router)
