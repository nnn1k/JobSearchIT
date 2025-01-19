from fastapi import Depends, HTTPException, status

from backend.utils.hash_pwd import HashPwd


async def register_user(user, repository):
    if await repository.get_one(email=user.email):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user is exist",
        )
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="password mismatch",
        )
    new_user = await repository.add_one(
        email=user.email,
        password=HashPwd.hash_password(user.password),
    )
    return new_user

async def login_user(user, repository):
    new_user = await repository.get_one(email=user.email)
    if not new_user or not HashPwd.validate_password(password=user.password, hashed_password=new_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )
    return new_user
