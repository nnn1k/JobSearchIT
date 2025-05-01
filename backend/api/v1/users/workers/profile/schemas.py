from datetime import date
from typing import Optional

from pydantic import BaseModel


class WorkerProfileSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    city: Optional[str] = None
