from fastapi import HTTPException, status


async def patch_dependencies(user, new_user, repository):
    keys = user.__fields__.keys()
    if new_user.key not in keys:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Key {new_user.key} not found."
        )
    if new_user.key in ('password', 'created_at', 'updated_at', 'id', 'email'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Key {new_user.key} is immutable"
        )
    update_data = {new_user.key: new_user.value}
    return await repository.update_one(id=user.id, **update_data)
