from typing import TypeVar

from pydantic import BaseModel

from backend.core.schemas.user_schema import UserResponseSchema

UserVar = TypeVar('UserVar', bound=UserResponseSchema)
BaseVar = TypeVar('BaseVar', bound=BaseModel)
