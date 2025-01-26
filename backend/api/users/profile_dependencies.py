from fastapi import HTTPException, status

from backend.api.users.employers.schemas import EmployerSchema
from backend.api.users.workers.schemas import WorkerSchema
from backend.schemas.global_schema import DynamicSchema


async def user_patch_dependencies(
        user: WorkerSchema or EmployerSchema,
        new_user: DynamicSchema,
        repository) -> WorkerSchema or EmployerSchema:
    user_keys = user.__fields__.keys()
    new_user_items = new_user.dict().items()
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

        if not isinstance(value, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Value {value} is not a string"
            )

    return await repository.update_one(id=user.id, **new_user.model_dump())
