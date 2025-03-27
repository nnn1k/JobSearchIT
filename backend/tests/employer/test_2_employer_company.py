import pytest

from backend.tests.employer.utils_test import cache_company, employer_client, get_company
from backend.core.schemas import CompanySchema


class TestEmployerCompany:

    @pytest.mark.asyncio
    async def test_create_company(self):
        client = await employer_client()
        response = await client.post(
            '/companies',
            json={
                "name": "test",
                "description": "test"
            }
        )

        assert response.status_code == 200
        company = response.json().get('company')
        assert company is not None
        company_schema = CompanySchema.model_validate(company, from_attributes=True)
        await cache_company(company_schema)

    @pytest.mark.asyncio
    async def test_get_company(self):
        client = await employer_client()
        company = await get_company()
        response = await client.get(
            f'/companies/{company.id}',
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_put_company(self):
        client = await employer_client()
        company = await get_company()
        response = await client.put(
            f'/companies/{company.id}',
            json={
                "description": "tttest",
            }
        )
        assert response.status_code == 200
