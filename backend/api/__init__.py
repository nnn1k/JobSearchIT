from fastapi import APIRouter

from backend.api.users import router as users_router
from backend.api.companies.views import router as company_router
from backend.api.vacancies.views import router as vacancies_router
from backend.api.professions.views import router as professions_router
from backend.api.resumes.views import router as resumes_router

from backend.api.skills.views import router as skills_router
from backend.database.utils.queries import check_connection_db
from backend.modules.redis.redis_utils import check_redis_connection, clear_redis

router = APIRouter(prefix="/api")

router.include_router(users_router)
router.include_router(company_router)
router.include_router(vacancies_router)
router.include_router(skills_router)
router.include_router(professions_router)
router.include_router(resumes_router)


test_router = APIRouter(prefix='/test', tags=['test'])

@test_router.get('/test_redis_connect')
async def test_redis_connect():
    await check_redis_connection()
    return {'status': 'ok'}


@test_router.get('/redis_clear')
async def redis_clear():
    await clear_redis()
    return {'status': 'ok'}

@test_router.get('/db_connect')
async def db_connect(
):
    await check_connection_db()
    return {'status': 'ok'}

router.include_router(test_router)