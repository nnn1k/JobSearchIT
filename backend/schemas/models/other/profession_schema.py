from pydantic import ConfigDict

from backend.schemas.global_schema import GlobalSchemaNoDate


class ProfessionSchema(GlobalSchemaNoDate):
    title: str

    model_config = ConfigDict(from_attributes=True)