from fastapi import APIRouter
from backend.api.users.auth import router as auth_router

router = APIRouter(prefix="/api")

router.include_router(auth_router)
