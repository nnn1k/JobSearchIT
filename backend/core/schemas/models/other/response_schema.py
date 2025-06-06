from typing import Optional

from backend.core.schemas.global_schema import GlobalSchema


class ResponseSchema(GlobalSchema):
    vacancy_id: int
    resume_id: int
    is_worker_accepted: Optional[bool] = None
    is_employer_accepted: Optional[bool] = None
    first: str


class ResponseSchemaRel(ResponseSchema):
    vacancy: 'VacancySchemaRel'
    resume: 'ResumeSchemaRel'
    chat: Optional['ChatSchema'] = None
