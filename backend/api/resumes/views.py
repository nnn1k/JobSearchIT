from fastapi import APIRouter, Depends

from backend.api.resumes.dependencies import (
    create_resume_dependencies,
    get_resume_dependencies,
    get_all_resumes_dependencies,
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
        'user': user,
        'resume': resume,
    }

@router.get('/{resume_id}', summary='Посмотреть одно резюме')
def get_one_resume_views(
        resume_and_user=Depends(get_resume_dependencies)
):
    resume, user, can_update = resume_and_user
    return {
        'status': 'ok',
        'user': user,
        'resume': resume,
        'can_update': can_update,
    }

@router.get('/', summary='Посмотреть все резюме')
def get_all_resumes_views(
        resume_and_user=Depends(get_all_resumes_dependencies)
):
    resumes, user, can_update = resume_and_user
    return {
        'status': 'ok',
        'user': user,
        'resumes': resumes,
        'can_update': can_update,
    }

@router.put('/{resume_id}', summary='Обновить резюме')
def update_resume_views(
        resume_and_user=Depends(update_resume_dependencies)
):
    resume, user = resume_and_user
    return {
        'status': 'ok',
        'user': user,
        'resume': resume,
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

