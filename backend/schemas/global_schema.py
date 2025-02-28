import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, validator
from fastapi import HTTPException, status


class GlobalSchemaNoDate(BaseModel):
    id: Optional[int] = None

    @validator('id')
    def check_id(cls, id, values):
        if id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='id must be greater than zero',
            )
        return id


class GlobalSchema(GlobalSchemaNoDate):
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class DynamicSchema(BaseModel):
    class Config:
        extra = 'allow'


class ValidateSalarySchema(BaseModel):
    profession_id: int
    salary_first: Optional[int] = None
    salary_second: Optional[int] = None

    @validator('salary_second')
    def check_second_salary(cls, salary_second, values):
        if not salary_second:
            return salary_second
        if salary_second < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Salary must be greater than zero'
            )
        if salary_second == 0:
            return None
        salary_first = values.get('salary_first')
        if not salary_first:
            return salary_second
        if salary_first > salary_second:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Salary first must be less than salary second',
            )
        return salary_second

    @validator('salary_first')
    def check_first_salary(cls, salary_first, values):
        if not salary_first:
            return salary_first
        if salary_first < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Salary must be greater than zero'
            )
        if salary_first == 0:
            return None
        return salary_first

    @validator('profession_id')
    def check_profession_id(cls, profession_id, values):
        if profession_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='profession_id must be greater than zero'
            )
        return profession_id
