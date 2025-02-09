from typing import TypeVar

from pydantic import BaseModel

from backend.schemas.user_schema import UserAbstractSchema

UserVar = TypeVar('UserVar', bound=UserAbstractSchema)
BaseVar = TypeVar('BaseVar', bound=BaseModel)
