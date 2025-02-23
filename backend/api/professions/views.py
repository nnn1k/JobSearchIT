from fastapi import APIRouter, Depends

from backend.api.professions.queries import get_professions_queries
from backend.utils.auth_utils.user_login_dependencies import get_user_by_token

router = APIRouter(prefix='/professions', tags=['professions'])

@router.get('', summary='Получить все профессии')
async def get_professions_views():
    professions = await get_professions_queries()
    return {
        'professions': professions,
        'status': 'ok'
    }

