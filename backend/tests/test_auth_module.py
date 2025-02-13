import pytest
from httpx import AsyncClient

from backend.utils.other.email_func import SendEmail

base_url = 'http://127.0.0.1:8000/api/'


@pytest.mark.asyncio
async def test_login_worker():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post("/auth/workers/login", json={
            "email": "user@example.com",
            "password": "string"
        })

    assert response.status_code == 200
    assert response.json().get('user') is not None


@pytest.mark.asyncio
async def test_register_worker():
    async with AsyncClient(base_url=base_url) as client:
        rand_code = SendEmail.get_random_code(k=8)

        response = await client.post("/auth/workers/register", json={
            "email":  rand_code + "test@example.com",
            "password": "string",
            "confirm_password": "string"
        })

    assert response.status_code == 200
    assert response.json().get('user') is not None

@pytest.mark.asyncio
async def test_login_employer():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post("/auth/employers/login", json={
            "email": "user@example.com",
            "password": "string"
        })

    assert response.status_code == 200
    assert response.json().get('user') is not None


@pytest.mark.asyncio
async def test_register_employer():
    async with AsyncClient(base_url=base_url) as client:
        rand_code = SendEmail.get_random_code(k=8)

        response = await client.post("/auth/employers/register", json={
            "email":  rand_code + "test@example.com",
            "password": "string",
            "confirm_password": "string"
        })

    assert response.status_code == 200
    assert response.json().get('user') is not None

