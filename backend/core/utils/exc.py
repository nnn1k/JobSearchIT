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

review_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='review not found'
)

user_have_company_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='user have company'
)
user_dont_have_company_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='user dont have company'
)

user_is_not_owner_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='user is not owner'
)

incorrect_user_type_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="incorrect user type",
)

response_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='response not found'
)

response_is_exist_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='response already exist'
)

invalid_token_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="invalid token",
)

chat_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='chat not found'
)
user_have_this_profession_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='user have object with this profession'
)

incorrect_login_or_password_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect login or password",
)

user_is_exist_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="user is exist",
)

password_mismatch_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="password mismatch",
)

incorrect_code_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect code",
)
