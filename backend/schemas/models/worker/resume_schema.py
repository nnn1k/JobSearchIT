from typing import Optional
from backend.schemas.global_schema import GlobalSchema
from backend.utils.str_const import RESUME_TYPE


class ResumeSchema(GlobalSchema):
    title: str
    description: str
    salary_first: Optional[int] = None
    salary_second: Optional[int] = None
    city: Optional[str] = None
    is_hidden: bool = False
    worker_id: int
    type: str = RESUME_TYPE

    worker: Optional['WorkerResponseSchema'] = None

