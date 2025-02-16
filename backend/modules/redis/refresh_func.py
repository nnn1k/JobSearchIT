from backend.modules.redis.redis_utils import cache_list_object
from backend.schemas import VacancySchema
from backend.utils.other.celery_utils import cl_app

from backend.api.users.employers.profile.queries import get_employer_by_id_queries
from backend.api.users.workers.profile.queries import get_worker_by_id_queries
from backend.api.vacancies.queries import get_vacancy_by_id_queries
from backend.api.companies.queries import get_company_by_id_queries
from backend.api.users.workers.resumes.queries import get_one_resume_by_id_queries


@cl_app.task
async def refresh_resume(resume_id: int, worker_id: int):
    get_one_resume_by_id_queries.delay(resume_id, refresh=True)
    get_worker_by_id_queries.delay(worker_id, refresh=True)


@cl_app.task
async def refresh_vacancy(vacancy_id: int, company_id: int, employer_id: int):
    get_vacancy_by_id_queries.delay(vacancy_id, refresh=True)
    get_company_by_id_queries.delay(company_id, refresh=True)
    get_employer_by_id_queries.delay(employer_id, refresh=True)


@cl_app.task
async def refresh_company(company_id: int, employer_id: int, vacancies: list[VacancySchema]):
    get_company_by_id_queries.delay(company_id, refresh=True)
    get_employer_by_id_queries.delay(employer_id, refresh=True)
    cache_list_object.delay(vacancies)


@cl_app.task
async def refresh_employer(employer_id: int):
    get_employer_by_id_queries.delay(employer_id, refresh=True)
