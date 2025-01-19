from fastapi import APIRouter
from .workers import worker_auth_router
from .employers import employers_auth_router


router = APIRouter(prefix="/auth")

router.include_router(worker_auth_router)
router.include_router(employers_auth_router)
