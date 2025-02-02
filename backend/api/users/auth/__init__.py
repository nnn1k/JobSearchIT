from fastapi import APIRouter, Response

from backend.utils.auth_utils.token_dependencies import ACCESS_TOKEN, REFRESH_TOKEN
from backend.api.users.auth.workers.views import router as worker_auth_router
from backend.api.users.auth.employers.views import router as employer_auth_router


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
router.include_router(employer_auth_router)
