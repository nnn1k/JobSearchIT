from typing import List

from pydantic import BaseModel, ConfigDict

from backend.schemas.global_schema import GlobalSchema


class SkillSchema(GlobalSchema):
    name: str

    model_config = ConfigDict(from_attributes=True)

class SkillListSchema(BaseModel):
    skills: List['SkillSchema']