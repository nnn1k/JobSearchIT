import pytest

from backend.tests.worker.utils import cache_resume, get_resume, worker_client
from backend.schemas.models.worker.resume_schema import ResumeSchema


class TestWorkerResume:

    @pytest.mark.asyncio
    async def test_create_resume(self):
        client = await worker_client()
        response = await client.post(
            '/workers/resumes',
            json={
                "title": "test",
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
        resume = response.json().get('resume')
        assert resume is not None
        resume_schema = ResumeSchema.model_validate(resume, from_attributes=True)
        await cache_resume(resume_schema)

    @pytest.mark.asyncio
    async def test_get_resume(self):
        client = await worker_client()
        resume = await get_resume()
        response = await client.get(
            f'/workers/resumes/{resume.id}',
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_put_resume(self):
        client = await worker_client()
        resume = await get_resume()
        response = await client.put(
            f'/workers/resumes/{resume.id}',
            json={
                "title": "testt",
                "description": "testt",
                "salary_first": 300,
                "salary_second": 400,
                "city": "testt"
            }
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_resume(self):
        client = await worker_client()
        resume = await get_resume()
        response = await client.delete(
            f'/workers/resumes/{resume.id}',
        )
        assert response.status_code == 200
