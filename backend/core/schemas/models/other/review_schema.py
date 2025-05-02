from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator

from backend.core.schemas.global_schema import GlobalSchema


class ReviewSchema(GlobalSchema):
    worker_id: int
    company_id: int
    score: int
    message: str


class ReviewCreate(BaseModel):
    score: int
    message: str

    @field_validator('score')
    def check_id(cls, score: int) -> int:
        if not (1 <= score <= 5):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='score must be between 1 and 5',
            )
        return score

