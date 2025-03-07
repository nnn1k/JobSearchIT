import pytest

from backend.tests.utils import check_user
from backend.tests.employer.utils_test import employer_client


class TestEmployerProfile:

    @pytest.mark.asyncio
    async def test_get_employer(self):
        client = await employer_client()
        response = await client.get(
            '/employers/me',
        )

        assert response.status_code == 200
        user = check_user(response)

    @pytest.mark.asyncio
    async def test_put_employer(self):
        client = await employer_client()
        response = await client.put(
            '/employers/me',
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
    async def test_patch_employer(self):
        client = await employer_client()
        response = await client.patch(
            '/employers/me',
            json={
                "name": "ttest",
            }
        )

        assert response.status_code == 200
        user = check_user(response)
        assert user.name == "ttest"
