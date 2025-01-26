from typing import Optional

from backend.schemas.global_schema import GlobalSchema

class ResumeSchema(GlobalSchema):
    title: str
    description: Optional[str] = None
    salary: Optional[str] = None
    worker_id: int
