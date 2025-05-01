from typing import Optional

from fastapi import Cookie, Depends, Query, Response
from jwt import ExpiredSignatureError

from backend.api.v1.users.auth.schemas import WorkerSchema, EmployerSchema
from backend.core.schemas import EmployerResponseSchema, WorkerResponseSchema
from backend.core.services.users.dependencies import get_user_serv
from backend.core.services.users.service import UserService
from backend.core.utils.classes.AuthJWT import jwt_token
from backend.core.utils.const import EMPLOYER_USER_TYPE, WORKER_USER_TYPE, ACCESS_TOKEN, REFRESH_TOKEN
from backend.core.utils.exc import invalid_token_exc, incorrect_user_type_exc
from backend.core.utils.logger_utils.logger_func import logger
from backend.core.utils.other.type_utils import UserVar


async def get_employer_by_token(
        response: Response,
        access_token=Cookie(None, include_in_schema=False),
        refresh_token=Cookie(None, include_in_schema=False),
        user_serv: UserService = Depends(get_user_serv)
) -> EmployerSchema:
    return await get_user_by_token(
        access_token=access_token,
        refresh_token=refresh_token,
        response=response,
        correct_user_type=EMPLOYER_USER_TYPE,
        user_serv=user_serv
    )


async def get_worker_by_token(
        response: Response,
        access_token=Cookie(None, include_in_schema=False),
        refresh_token=Cookie(None, include_in_schema=False),
        user_serv: UserService = Depends(get_user_serv)
) -> WorkerSchema:
    return await get_user_by_token(
        access_token=access_token,
        refresh_token=refresh_token,
        response=response,
        correct_user_type=WORKER_USER_TYPE,
        user_serv=user_serv
    )


async def get_user_by_token(
        access_token: Optional[str] = Cookie(None, include_in_schema=False),
        refresh_token: Optional[str] = Cookie(None, include_in_schema=False),
        response: Response = None,
        correct_user_type: Optional[str] = Query(None, include_in_schema=False),
        user_serv: UserService = Depends(get_user_serv)
) -> Optional[UserVar]:
    """
    ЕСЛИ correct_user_type = None ТО пользователь может быть worker|employer|guest(no type)
    ЕСЛИ correct_user_type указать(worker|employer), ТО пользователь может быть только тот тип, иначе incorrect_user_type_exc
    """
    user_id: int | None = None
    user_type: str | None = None
    if access_token:
        try:
            user_id = jwt_token.decode_jwt(token=access_token).get("sub")
            user_type = jwt_token.decode_jwt(token=access_token).get("type")
        except ExpiredSignatureError:
            logger.info('access token expired')
    if not user_id and refresh_token:
        try:
            new_access_token, new_refresh_token = jwt_token.token_refresh(refresh_token)
            if not (new_access_token and new_refresh_token):
                raise invalid_token_exc

            user_id = jwt_token.decode_jwt(token=new_access_token).get("sub")
            if not user_id:
                raise invalid_token_exc

            response.set_cookie(key=ACCESS_TOKEN, value=new_access_token)
            response.set_cookie(key=REFRESH_TOKEN, value=new_refresh_token)
        except ExpiredSignatureError:
            raise invalid_token_exc
    if correct_user_type is not None and correct_user_type != user_type:
        raise incorrect_user_type_exc
    if user_type == WORKER_USER_TYPE:
        return await user_serv.get_worker_by_id(id=int(user_id))
    elif user_type == EMPLOYER_USER_TYPE:
        return await user_serv.get_employer_by_id(id=int(user_id))
    else:
        raise incorrect_user_type_exc


async def get_auth_user_by_token(
        response: Response,
        access_token=Cookie(None, include_in_schema=False),
        refresh_token=Cookie(None, include_in_schema=False),
        user_serv: UserService = Depends(get_user_serv)
) -> UserVar:
    user = await get_user_by_token(
        access_token=access_token,
        refresh_token=refresh_token,
        response=response,
        correct_user_type=None,
        user_serv=user_serv
    )
    if user is None:
        raise invalid_token_exc
    return user
