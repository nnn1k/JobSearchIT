from fastapi import APIRouter, Depends


from backend.core.services.professions.dependencies import get_prof_serv
from backend.core.services.professions.service import ProfessionService

router = APIRouter(prefix='/professions', tags=['professions'])


@router.get('', summary='Получить все профессии')
async def get_professions_views(
        prof_serv: ProfessionService = Depends(get_prof_serv)
):
    professions = await prof_serv.get_professions()
    return {
        'professions': professions,
        'status': 'ok'
    }

