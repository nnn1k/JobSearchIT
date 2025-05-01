from fastapi import APIRouter


from backend.api.test_router import test_router

# start v1
from backend.api.v1.users.router import router as users_router
from backend.api.v1.companies.views import router as company_router
from backend.api.v1.vacancies.views import router as vacancies_router
from backend.api.v1.professions.views import router as professions_router
from backend.api.v1.resumes.views import router as resumes_router
from backend.api.v1.chats.views import router as chats_router

from backend.api.v1.skills.views import router as skills_router
from backend.api.v1.responses.views import router as responses_router
# end v1

api_router = APIRouter(prefix="/api")
v2_router = APIRouter(prefix="/v2", tags=['api_v2'])

# start v1
api_router.include_router(users_router)
api_router.include_router(company_router)
api_router.include_router(vacancies_router)
api_router.include_router(skills_router)
api_router.include_router(professions_router)
api_router.include_router(resumes_router)
api_router.include_router(responses_router)
api_router.include_router(chats_router)
# end v1

# start v2


# end v2

api_router.include_router(test_router)
api_router.include_router(v2_router)
