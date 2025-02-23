import pytest

from backend.modules.redis.redis_code_utils import get_code_from_redis
from backend.tests.utils import async_client, check_token, check_user, test_user
from backend.tests.employer.utils_test import cache_employer, employer_client, get_employer
from backend.utils.const import EMPLOYER_USER_TYPE
from backend.utils.other.logger_utils import logger


class TestEmployerAuth:

    @pytest.mark.asyncio
    async def test_register_employer(self):
        logger.debug('\n\nTEST STARTED\n\n')
        client = async_client()
        response = await client.post("/auth/employers/register", json=test_user)

        assert response.status_code == 200
        user = check_user(response)
        token = check_token(response)
        await cache_employer(user, token)

    @pytest.mark.asyncio
    async def test_login_employer(self):
        client = async_client()
        response = await client.post("/auth/employers/login", json=test_user)

        assert response.status_code == 200
        user = check_user(response)
        token = check_token(response)
        await cache_employer(user, token)


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
