from pydantic import BaseModel

from backend.schemas.global_schema import GlobalSchema


class SkillSchema(GlobalSchema):
    name: str


class SkillsResponseSchema(BaseModel):
    id: int
    name: str
