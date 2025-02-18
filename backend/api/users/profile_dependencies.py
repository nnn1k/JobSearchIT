from fastapi import HTTPException, status

from backend.schemas.global_schema import DynamicSchema
from backend.utils.other.type_utils import UserVar


async def user_patch_dependencies(
        user: UserVar,
        new_user: DynamicSchema,
        repository) -> UserVar:
    user_keys = user.model_dump().keys()
    new_user_items = new_user.model_dump().items()
    for key, value in new_user_items:

        if key not in user_keys:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Key {key} not found."
            )
        if key in ('password', 'created_at', 'updated_at', 'deleted_at', 'id', 'email'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Key {key} is immutable"
            )

    user = await repository.update_one(id=user.id, **new_user.model_dump())
    return user
