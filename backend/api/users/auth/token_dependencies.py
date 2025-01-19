from fastapi import HTTPException, status

from backend.api.users.auth.AuthJWT import jwt_token

ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'


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