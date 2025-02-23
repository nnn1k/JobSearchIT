import pytest

from backend.tests.utils import check_user
from backend.tests.worker.utils_test import worker_client


class TestWorkerProfile:

    @pytest.mark.asyncio
    async def test_get_worker(self):
        client = await worker_client()
        response = await client.get(
            '/workers/me',
        )

        assert response.status_code == 200
        user = check_user(response)
        assert user.name == ''

    @pytest.mark.asyncio
    async def test_put_worker(self):
        client = await worker_client()
        response = await client.put(
            '/workers/me',
            json={
                "name": "test",
                "surname": "test",
                "patronymic": "test",
                "phone": "test",
                "birthday": "2025-02-15",
                "city": "test"
            }
        )

        assert response.status_code == 200
        user = check_user(response)
        assert user.name == "test"

    @pytest.mark.asyncio
    async def test_patch_worker(self):
        client = await worker_client()
        response = await client.patch(
            '/workers/me',
            json={
                "name": "ttest",
            }
        )

        assert response.status_code == 200
        user = check_user(response)
        assert user.name == 'ttest'
