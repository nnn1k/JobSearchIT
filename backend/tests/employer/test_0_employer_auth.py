import pytest

from backend.modules.redis.redis_utils import cache_object, get_code_from_redis
from backend.tests.utils import async_client, check_token, check_user, employer_client, get_employer, test_user
from backend.utils.str_const import EMPLOYER_USER_TYPE


class TestEmployerAuth:

    @pytest.mark.asyncio
    async def test_register_employer(self):
        client = async_client()
        response = await client.post("/auth/employers/register", json=test_user)

        assert response.status_code == 200
        user = check_user(response)
        token = check_token(response)
        await cache_object(
            obj_id=1,
            obj_type='test_employer',
            obj=user
        )
        await cache_object(
            obj_id=1,
            obj_type='test_employer_token',
            obj=token
        )

    @pytest.mark.asyncio
    async def test_login_employer(self):
        client = async_client()
        response = await client.post("/auth/employers/login", json=test_user)

        assert response.status_code == 200
        check_user(response)

    @pytest.mark.asyncio
    async def test_get_code_employer(self):
        client = await employer_client()
        response = await client.get("/auth/employers/code")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_post_code_employer(self):
        client = await employer_client()
        employer = await get_employer()
        code = await get_code_from_redis(user_type=EMPLOYER_USER_TYPE, user_id=employer.id)
        response = await client.post("/auth/employers/code", json={'code': code})

        assert response.status_code == 200
