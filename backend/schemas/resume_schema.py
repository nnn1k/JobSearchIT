from typing import Optional
from backend.schemas.global_schema import GlobalSchema


class ResumeSchema(GlobalSchema):
    title: str
    description: str
    salary_first: Optional[int] = None
    salary_second: Optional[int] = None
    city: Optional[str] = None
    is_hidden: bool = False
    worker_id: int

    worker: Optional['WorkerResponseSchema'] = None

