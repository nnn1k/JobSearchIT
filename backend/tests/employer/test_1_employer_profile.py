import pytest

from backend.tests.utils import check_user, employer_client


class TestEmployerProfile:

    @pytest.mark.asyncio
    async def test_get_employer(self):
        client = await employer_client()
        response = await client.get(
            '/employers/me',
        )

        assert response.status_code == 200
        check_user(response)

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
        check_user(response)

    @pytest.mark.asyncio
    async def test_patch_employer(self):
        client = await employer_client()
        response = await client.patch(
            '/employers/me',
            json={
                "name": "test",
            }
        )

        assert response.status_code == 200
        check_user(response)
