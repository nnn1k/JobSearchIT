from fastapi import APIRouter, Depends

from backend.api.professions.queries import get_professions_queries

router = APIRouter(prefix='/professions', tags=['professions'])

@router.get('', summary='Получить все профессии')
async def get_professions_views():
    professions = await get_professions_queries()
    return {
        'professions': professions,
        'status': 'ok'
    }

