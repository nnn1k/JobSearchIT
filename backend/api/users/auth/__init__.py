from fastapi import APIRouter, Response

from .token_dependencies import ACCESS_TOKEN, REFRESH_TOKEN
from .workers import worker_auth_router
from .employers import employers_auth_router


router = APIRouter(prefix="/auth")

@router.post('/logout', summary='Выход с аккаунта')
def logout_user(response: Response):
    response.delete_cookie(ACCESS_TOKEN)
    response.delete_cookie(REFRESH_TOKEN)
    response.delete_cookie('user_type')
    return {
        'status': 'ok'
    }


router.include_router(worker_auth_router)
router.include_router(employers_auth_router)
