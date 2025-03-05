from typing import Optional

from backend.schemas.global_schema import GlobalSchema


class ResponseSchema(GlobalSchema):
    vacancy_id: int
    resume_id: int
    is_worker_accepted: Optional[bool] = None
    is_employer_accepted: Optional[bool] = None
