from pydantic import ConfigDict

from backend.core.schemas.global_schema import GlobalSchemaNoDate


class ProfessionSchema(GlobalSchemaNoDate):
    title: str

    model_config = ConfigDict(from_attributes=True)
