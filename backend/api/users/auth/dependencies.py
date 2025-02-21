from typing import Any, Dict

from fastapi import HTTPException, Response
from starlette import status

from backend.api.users.auth.classes.AuthJWT import Token, jwt_token
from backend.api.users.auth.schemas import UserType
from backend.database.models.employer import EmployersOrm
from backend.database.models.worker import WorkersOrm
from backend.schemas import EmployerResponseSchema, WorkerResponseSchema
from backend.utils.const import ACCESS_TOKEN, REFRESH_TOKEN


def get_login_db_model(user_type: UserType):
    match user_type:
        case UserType.employer:
            return EmployersOrm, EmployerResponseSchema
        case UserType.worker:
            return WorkersOrm, WorkerResponseSchema
        case _:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")


def create_token(response: Response, user) -> Dict[str, Any]:
    access_token = jwt_token.create_access_token(id=user.id, user_type=user.type)
    refresh_token = jwt_token.create_refresh_token(id=user.id, user_type=user.type)

    response.set_cookie(ACCESS_TOKEN, access_token, max_age=60*60*24*365)
    response.set_cookie(REFRESH_TOKEN, refresh_token, max_age=60*60*24*365)
    response.set_cookie('user_type', user.type, max_age=60*60*24*365)
    token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    return {
        'user': user,
        'token': token,
        'status': 'ok'
    }
