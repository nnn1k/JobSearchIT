from fastapi import APIRouter, Depends

from backend.api.users.workers.resumes.dependencies import (
    create_resume_dependencies,
    get_one_resume_dependencies,
    update_resume_dependencies,
    delete_resume_dependencies
)

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post('/', summary='Создать резюме')
def add_resumes_views(
        resume_and_user=Depends(create_resume_dependencies)
):
    resume, user = resume_and_user
    return {
        'status': 'ok',
        'resume': resume,
        'user': user,
    }


@router.get('/{resume_id}', summary='Посмотреть одно резюме')
def get_one_resume_views(
        resume_and_user=Depends(get_one_resume_dependencies)
):
    resume, user, can_update = resume_and_user
    return {
        'status': 'ok',
        'resume': resume,
        'can_update': can_update,
        'user': user,
    }


@router.put('/{resume_id}', summary='Обновить резюме')
def update_resume_views(
        resume_and_user=Depends(update_resume_dependencies)
):
    resume, user = resume_and_user
    return {
        'status': 'ok',
        'resume': resume,
        'user': user,
        'message': 'resume updated'
    }


@router.delete('/{resume_id}', summary='Удалить резюме')
def delete_resume_views(
        resume_and_user=Depends(delete_resume_dependencies)
):
    resume, user = resume_and_user
    return {
        'status': 'ok',
        'user': user,
        'message': 'resume deleted'
    }
