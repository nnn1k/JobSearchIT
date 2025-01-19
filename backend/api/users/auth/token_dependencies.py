from fastapi import HTTPException, status, Cookie


from backend.api.users.auth.AuthJWT import jwt_token
from backend.api.users.employers.repository import get_employer_repo
from backend.api.users.employers.schemas import EmployerSchema
from backend.api.users.workers.repository import get_worker_repo
from backend.api.users.workers.schemas import WorkerSchema

ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'

async def get_worker_by_token(
    access_token=Cookie(None),
) -> WorkerSchema:
    worker_repo = get_worker_repo()
    return await get_user_by_token(access_token, worker_repo, WorkerSchema)

async def get_employer_by_token(
    access_token=Cookie(None),
) -> EmployerSchema:
    employer_repo = get_employer_repo()
    return await get_user_by_token(access_token, employer_repo, EmployerSchema)

async def get_user_by_token(access_token, repository, schema):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"not access token",
        )
    try:
        user_id = jwt_token.decode_jwt(token=access_token).get("sub")
        user = await repository.get_one(id=int(user_id))
        if user:
            return schema.model_validate(user, from_attributes=True)
    except Exception as e:
        print(e)
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token (access)",
        )