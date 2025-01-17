from fastapi import Cookie, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from backend.api.users.auth.AuthJWT import jwt_token
ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'

def get_user(id):
    return ...

class UserResponseModel(BaseModel):
    pass

def get_user_by_token(
    access_token=Cookie(None),
    refresh_token=Cookie(None),
    request: Request = None,
) -> UserResponseModel:
    if access_token is None:
        check_refresh_token(refresh_token)
    try:
        user_id = jwt_token.decode_jwt(token=access_token).get("sub")
        user = get_user(id=user_id)
        if user:
            return UserResponseModel.model_validate(user, from_attributes=True)
    except Exception:
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
