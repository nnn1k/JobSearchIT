from backend.api.v1.users.auth.classes.AuthJWT import jwt_token
from backend.api.v1.users.auth.classes.HashPwd import HashPwd
from backend.api.v1.users.auth.schemas import LoginSchema, WorkerSchema, EmployerSchema
from backend.core.services.auth.repository import AuthRepository
from fastapi import Response

from backend.core.utils.const import ACCESS_TOKEN, REFRESH_TOKEN
from backend.core.utils.exc import incorrect_login_or_password_exc
from backend.core.utils.other.type_utils import UserVar


class AuthService:

    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo

    async def login_worker(self, login_schema: LoginSchema, response: Response):
        worker = await self.auth_repo.get_worker_by_email(email=login_schema.email)
        if not worker:
            raise incorrect_login_or_password_exc
        if not HashPwd.validate_password(
                password=login_schema.password,
                hashed_password=worker.password
        ):
            raise incorrect_login_or_password_exc
        schema = WorkerSchema.model_validate(worker)
        self._create_token(response=response, user=schema)
        return schema

    async def login_employer(self, login_schema: LoginSchema, response: Response):
        employer = await self.auth_repo.get_employer_by_email(email=login_schema.email)
        if not employer:
            raise incorrect_login_or_password_exc
        if not HashPwd.validate_password(
            password=login_schema.password,
            hashed_password=employer.password
        ):
            raise incorrect_login_or_password_exc
        schema = EmployerSchema.model_validate(employer)
        self._create_token(response=response, user=schema)
        return schema

    @staticmethod
    def _create_token(response: Response, user: UserVar):
        access_token = jwt_token.create_access_token(user_id=user.id, user_type=user.type)
        refresh_token = jwt_token.create_refresh_token(user_id=user.id, user_type=user.type)

        response.set_cookie(ACCESS_TOKEN, access_token, max_age=60 * 60 * 24 * 365)
        response.set_cookie(REFRESH_TOKEN, refresh_token, max_age=60 * 60 * 24 * 365)
        response.set_cookie('user_type', user.type, max_age=60 * 60 * 24 * 365)