from fastapi import HTTPException, status, Cookie, Response
from fastapi.responses import RedirectResponse

from backend.api.users.auth.AuthJWT import jwt_token
from backend.api.users.workers.repository import get_worker_repo
from backend.api.users.workers.schemas import WorkerSchema

ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'

async def get_worker_by_token(
    access_token=Cookie(None),
) -> WorkerSchema:
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"not access token",
        )
    try:
        worker_id = jwt_token.decode_jwt(token=access_token).get("sub")
        worker_repo = get_worker_repo()
        worker = await worker_repo.get_one(id=int(worker_id))
        if worker:
            return WorkerSchema.model_validate(worker, from_attributes=True)
    except Exception as e:
        print(e)
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token (access)",
        )

