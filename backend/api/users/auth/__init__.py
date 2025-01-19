from fastapi import APIRouter
from .workers import worker_auth_router as worker_router


router = APIRouter(prefix="/auth")

router.include_router(worker_router)
