import pytest

from backend.modules.redis.redis_code_utils import get_code_from_redis
from backend.tests.utils import async_client, check_token, check_user, test_user
from backend.tests.worker.utils_test import cache_worker, get_worker, worker_client
from backend.utils.const import WORKER_USER_TYPE


class TestWorkerAuth:

    @pytest.mark.asyncio
    async def test_register_worker(self):
        client = async_client()
        response = await client.post("/auth/workers/register", json=test_user)

        assert response.status_code == 200
        user = check_user(response)
        token = check_token(response)
        await cache_worker(user, token)

    @pytest.mark.asyncio
    async def test_login_worker(self):
        client = async_client()
        response = await client.post("/auth/workers/login", json=test_user)

        assert response.status_code == 200
        user = check_user(response)
        token = check_token(response)
        await cache_worker(user, token)

    @pytest.mark.asyncio
    async def test_get_code_worker(self):
        client = await worker_client()
        response = await client.get("/auth/workers/code")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_post_code_worker(self):
        client = await worker_client()
        worker = await get_worker()
        code = await get_code_from_redis(user_type=WORKER_USER_TYPE, user_id=worker.id)
        response = await client.post("/auth/workers/code", json={'code': code})

        assert response.status_code == 200
