from typing import List

from pydantic import BaseModel

from backend.schemas.global_schema import GlobalSchema


class SkillSchema(GlobalSchema):
    name: str

class SkillListSchema(BaseModel):
    skills: List['SkillSchema']