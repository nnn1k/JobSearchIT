from pydantic import BaseModel


class CompanyAddSchema(BaseModel):
    name: str
    description: str


class CompanyUpdateSchema(BaseModel):
    description: str
