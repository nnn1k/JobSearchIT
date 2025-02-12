from sqlalchemy import select

from backend.api.users.auth.classes.HashPwd import HashPwd
from backend.database.settings.database import session_factory


async def login_user_queries(user, user_table, response_schema):
    async with session_factory() as session:
        login_user = await session.execute(select(user_table).filter_by(email=user.email))
        login_user = login_user.scalars().one_or_none()
        if not login_user or not HashPwd.validate_password(password=user.password, hashed_password=login_user.password):
            return None
        return response_schema.model_validate(login_user, from_attributes=True)

async def register_user_queries(user, user_table, response_schema):
    async with session_factory() as session:
        check_user = await session.execute(select(user_table).filter_by(email=user.email))
        check_user = check_user.scalars().one_or_none()
        if check_user:
            return None
        register_user = user_table(email=user.email, password=HashPwd.hash_password(user.password))
        session.add(register_user)
        await session.flush()
        await session.refresh(register_user)
        schema = response_schema.model_validate(register_user, from_attributes=True)
        await session.commit()
        return schema

async def update_code_queries(user_id: int, user_table, response_schema):
    async with session_factory() as session:
        update_user = await session.execute(select(user_table).filter_by(id=user_id))
        update_user = update_user.scalars().one_or_none()
        if not update_user:
            return None
        update_user.is_confirmed = True
        schema = response_schema.model_validate(update_user, from_attributes=True)
        await session.commit()
        return schema
