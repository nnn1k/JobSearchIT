from fastapi import HTTPException, status

from backend.core.utils.classes.AuthJWT import jwt_token
from backend.core.schemas.user_schema import UserTypeSchema
from backend.core.utils.const import ACCESS_TOKEN, REFRESH_TOKEN


async def check_user_role(access_token, refresh_token, response) -> UserTypeSchema | None:
    if access_token is None:
        return check_refresh_token(refresh_token, response)
    try:
        user_id = jwt_token.decode_jwt(token=access_token).get("sub")
        user_type = jwt_token.decode_jwt(token=access_token).get("type")
        return UserTypeSchema(id=user_id, type=user_type)
    except Exception:
        return check_refresh_token(refresh_token, response)


def check_refresh_token(refresh_token, response):
    if refresh_token is None:
        return None
    try:
        new_access_token, new_refresh_token = jwt_token.token_refresh(refresh_token)
        if new_access_token is None or new_refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token (refresh)",
            )

        response.set_cookie(key=ACCESS_TOKEN, value=new_access_token)
        response.set_cookie(key=REFRESH_TOKEN, value=new_refresh_token)
        user_id = jwt_token.decode_jwt(token=new_access_token).get("sub")
        user_type = jwt_token.decode_jwt(token=new_access_token).get("type")
        return UserTypeSchema(id=user_id, type=user_type)
    except Exception:
        return None
