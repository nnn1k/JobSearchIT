from backend.core.utils.classes.AuthJWT import jwt_token
from backend.core.utils.classes.HashPwd import HashPwd
from backend.core.schemas.user_schema import LoginSchema, RegisterSchema
from backend.core.schemas.models.employer.employer_schema import EmployerSchema
from backend.core.schemas import WorkerSchema
from backend.core.services.users.repository import UserRepository
from fastapi import Response

from backend.core.utils.const import ACCESS_TOKEN, REFRESH_TOKEN
from backend.core.utils.exc import incorrect_login_or_password_exc, user_is_exist_exc, password_mismatch_exc, \
    incorrect_code_exc
from backend.core.utils.other.type_utils import UserVar
from backend.core.utils.redis_utils.redis_code_utils import get_code_from_redis


class AuthService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def login_worker(self, login_schema: LoginSchema, response: Response) -> WorkerSchema:
        worker = await self.user_repo.get_worker(email=login_schema.email)
        if not worker:
            raise incorrect_login_or_password_exc
        if not HashPwd.validate_password(
                password=login_schema.password,
                hashed_password=worker.password
        ):
            raise incorrect_login_or_password_exc
        schema = WorkerSchema.model_validate(worker)
        self.create_token(response=response, user=schema)
        return schema

    async def login_employer(self, login_schema: LoginSchema, response: Response) -> EmployerSchema:
        employer = await self.user_repo.get_employer(email=login_schema.email)
        if not employer:
            raise incorrect_login_or_password_exc
        if not HashPwd.validate_password(
                password=login_schema.password,
                hashed_password=employer.password
        ):
            raise incorrect_login_or_password_exc
        schema = EmployerSchema.model_validate(employer)
        self.create_token(response=response, user=schema)
        return schema

    async def register_worker(self, reg_schema: RegisterSchema, response: Response) -> WorkerSchema:
        if reg_schema.password != reg_schema.confirm_password:
            raise password_mismatch_exc
        check_worker = await self.user_repo.get_worker(email=reg_schema.email)
        if check_worker:
            raise user_is_exist_exc
        worker = await self.user_repo.create_worker(
            email=reg_schema.email,
            password=HashPwd.hash_password(reg_schema.password)
        )
        schema = WorkerSchema.model_validate(worker)
        self.create_token(response=response, user=schema)
        return schema

    async def register_employer(self, reg_schema: RegisterSchema, response: Response) -> EmployerSchema:
        if reg_schema.password != reg_schema.confirm_password:
            raise password_mismatch_exc
        check_employer = await self.user_repo.get_employer(email=reg_schema.email)
        if check_employer:
            raise user_is_exist_exc
        employer = await self.user_repo.create_employer(
            email=reg_schema.email,
            password=HashPwd.hash_password(reg_schema.password)
        )
        schema = EmployerSchema.model_validate(employer)
        self.create_token(response=response, user=schema)
        return schema

    async def confirm_worker(self, code: str, user: WorkerSchema) -> WorkerSchema:
        new_code = await get_code_from_redis(user_type=user.type, user_id=user.id)
        if code != new_code:
            raise incorrect_code_exc
        new_user = await self.user_repo.update_worker(id=user.id, is_confirmed=True)
        schema = WorkerSchema.model_validate(new_user)
        return schema

    async def confirm_employer(self, code: str, user: EmployerSchema) -> EmployerSchema:
        new_code = await get_code_from_redis(user_type=user.type, user_id=user.id)
        if code != new_code:
            raise incorrect_code_exc
        new_user = await self.user_repo.update_employer(id=user.id, is_confirmed=True)
        schema = EmployerSchema.model_validate(new_user)
        return schema

    @staticmethod
    def create_token(response: Response, user: UserVar) -> None:
        access_token = jwt_token.create_access_token(user_id=user.id, user_type=user.type)
        refresh_token = jwt_token.create_refresh_token(user_id=user.id, user_type=user.type)

        response.set_cookie(ACCESS_TOKEN, access_token, max_age=60 * 60 * 24 * 365)
        response.set_cookie(REFRESH_TOKEN, refresh_token, max_age=60 * 60 * 24 * 365)
        response.set_cookie('user_type', user.type, max_age=60 * 60 * 24 * 365)
