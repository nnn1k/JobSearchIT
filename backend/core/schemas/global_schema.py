import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from fastapi import HTTPException, status


class GlobalSchemaNoDate(BaseModel):
    id: int

    @field_validator('id')
    def check_id(cls, id: int) -> int:
        if id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='id must be greater than zero',
            )
        return id

    model_config = ConfigDict(from_attributes=True)


class GlobalSchema(GlobalSchemaNoDate):
    created_at: Optional[datetime.datetime] = Field(default=None, strict=False)
    updated_at: Optional[datetime.datetime] = Field(default=None, strict=False)


class DynamicSchema(BaseModel):
    class Config:
        extra = 'allow'


class ValidateSalarySchema(BaseModel):
    profession_id: int
    salary_first: Optional[int] = 0
    salary_second: Optional[int] = 0

    @field_validator('salary_second')
    def check_second_salary(cls, salary_second: float | None, values: dict) -> float | None:
        if salary_second is None:
            return salary_second
        if salary_second < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Salary must be greater than zero'
            )
        if salary_second == 0:
            return None
        salary_first = values.data.get('salary_first')
        if salary_first is not None and salary_first > salary_second:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Salary first must be less than salary second',
            )
        return salary_second

    @field_validator('salary_first')
    def check_first_salary(cls, salary_first: float | None) -> float | None:
        if salary_first is None:
            return salary_first
        if salary_first < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Salary must be greater than zero'
            )
        if salary_first == 0:
            return None
        return salary_first

    @field_validator('profession_id')
    def check_profession_id(cls, profession_id: int) -> int:
        if profession_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='profession_id must be greater than zero'
            )
        return profession_id
