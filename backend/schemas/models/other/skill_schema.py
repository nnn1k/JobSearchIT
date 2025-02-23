from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from backend.schemas.global_schema import GlobalSchemaNoDate


class SkillSchema(GlobalSchemaNoDate):
    name: str

    model_config = ConfigDict(from_attributes=True)

class SkillListSchema(BaseModel):
    skills: List[Optional['SkillSchema']]
