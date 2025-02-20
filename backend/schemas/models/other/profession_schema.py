from pydantic import ConfigDict

from backend.schemas.global_schema import GlobalSchema


class ProfessionSchema(GlobalSchema):
    title: str

    model_config = ConfigDict(from_attributes=True)