from httpx import AsyncClient
from backend.api.users.auth.classes.AuthJWT import Token
from backend.schemas.user_schema import UserResponseSchema

base_url = 'http://127.0.0.1:8000/api/'

test_user = {
    "email": "tttest@example.com",
    "password": "string",
    "confirm_password": "string"
}


def async_client():
    return AsyncClient(
        base_url=base_url,
        timeout=10.0
    )


def check_user(response):
    user = response.json().get('user')
    user_schema = UserResponseSchema.model_validate(user)
    assert user is not None
    assert isinstance(user_schema, UserResponseSchema)
    return user_schema


def check_token(response):
    token = response.json().get('token')
    token_schema = Token.model_validate(token)
    assert token is not None
    assert isinstance(token_schema, Token)
    return token_schema


