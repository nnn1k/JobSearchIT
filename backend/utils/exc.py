from fastapi import HTTPException, status

company_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='company not found'
)

vacancy_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='vacancy not found'
)

employer_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='employer not found'
)

worker_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='worker not found'
)

resume_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='resume not found'
)

user_have_company_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='user have company'
)

user_is_not_owner_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='user is not owner'
)
