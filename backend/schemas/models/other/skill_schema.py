from typing import List

from pydantic import BaseModel

from backend.schemas.global_schema import GlobalSchema
from backend.utils.str_const import SKILL_TYPE


class SkillSchema(GlobalSchema):
    name: str
    type: str = SKILL_TYPE

class SkillListSchema(BaseModel):
    skills: List['SkillSchema']