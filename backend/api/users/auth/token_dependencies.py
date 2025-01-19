from fastapi import HTTPException, status, Cookie
from fastapi.responses import RedirectResponse

from backend.api.users.auth.AuthJWT import jwt_token
from backend.api.users.workers.repository import get_worker_repo
from backend.api.users.workers.schemas import WorkerSchema

ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'

async def get_worker_by_token(
    access_token=Cookie(None),
    refresh_token=Cookie(None),
) -> WorkerSchema:
    if access_token is None:
        check_refresh_token(refresh_token)
    try:
        worker_id = jwt_token.decode_jwt(token=access_token).get("sub")
        worker_repo = get_worker_repo()
        worker = await worker_repo.get_one(id=int(worker_id))
        if worker:
            return WorkerSchema.model_validate(worker, from_attributes=True)
    except Exception as e:
        print(e)
        check_refresh_token(refresh_token)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"not authenticated",
    )

def check_refresh_token(refresh_token):
    login_url = "/api/auth/login"
    if refresh_token is None:
        return RedirectResponse(url=login_url)
    try:
        new_access_token, new_refresh_token = jwt_token.token_refresh(refresh_token)
        if new_access_token is None or new_refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token (refresh)",
            )
        response = RedirectResponse(url='/')
        response.set_cookie(key=ACCESS_TOKEN, value=new_access_token)
        response.set_cookie(key=REFRESH_TOKEN, value=new_refresh_token)
        return response
    except Exception:
        return RedirectResponse(url=login_url)
