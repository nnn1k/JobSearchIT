from collections import Counter

from fastapi import APIRouter, Depends, Query

from backend.api.resumes.queries import get_all_resumes_query
from backend.utils.auth_utils.user_login_dependencies import get_user_by_token

router = APIRouter(
    prefix="/resumes",
    tags=["resumes"],
)

@router.get('', summary='Поиск по всем резюме')
async def get_resumes_views(
    user=Depends(get_user_by_token),
    max_salary: int = Query(None, ge=0),
    profession: str = None,
    city: str = None,
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0),

):
    resumes, params = await get_all_resumes_query(
        user=user,
        max_salary=max_salary,
        profession=profession,
        city=city,
    )
    cities = Counter(resume.city for resume in resumes)
    user_type = user.type if user else None
    return {
        'params': params,
        'count': len(resumes),
        'user_type': user_type,
        'cities': cities,
        'status': 'ok',
        'resumes': resumes[(page - 1) * size:page * size],
    }

