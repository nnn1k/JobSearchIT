import pytest

from backend.schemas import VacancySchema
from backend.tests.employer.utils_test import cache_vacancy, employer_client, get_vacancy


class TestEmployerVacancy:

    @pytest.mark.asyncio
    async def test_create_vacancy(self):
        client = await employer_client()
        response = await client.post(
            '/vacancy',
            json={
                "profession_id": 1,
                "description": "test",
                "salary_first": 100,
                "salary_second": 200,
                "city": "test",
                "skills": [
                    {
                        "id": 1,
                        "created_at": "2025-02-17T01:20:05.597Z",
                        "updated_at": "2025-02-17T01:20:05.597Z",
                        "deleted_at": "2025-02-17T01:20:05.598Z",
                        "name": "Python"
                    }
                ]
            }
        )
        assert response.status_code == 200
        vacancy = response.json().get('vacancy')
        assert vacancy is not None
        vacancy_schema = VacancySchema.model_validate(vacancy, from_attributes=True)
        await cache_vacancy(vacancy_schema)

    @pytest.mark.asyncio
    async def test_get_vacancy(self):
        client = await employer_client()
        vacancy = await get_vacancy()
        response = await client.get(
            f'/vacancy/{vacancy.id}',
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_put_vacancy(self):
        client = await employer_client()
        vacancy = await get_vacancy()
        response = await client.put(
            f'/vacancy/{vacancy.id}',
            json={
                "profession_id": 5,
                "description": "testt",
                "salary_first": 300,
                "salary_second": 400,
                "city": "testt"
            }
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_vacancy(self):
        client = await employer_client()
        vacancy = await get_vacancy()
        response = await client.delete(
            f'/vacancy/{vacancy.id}',
        )
        assert response.status_code == 200
