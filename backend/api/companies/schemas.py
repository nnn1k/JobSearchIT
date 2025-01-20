from pydantic import BaseModel

from backend.schemas.global_schema import GlobalSchema

class CompanySchema(GlobalSchema):
    name: str
    description: str


class CompanyAddSchema(BaseModel):
    name: str
    description: str
