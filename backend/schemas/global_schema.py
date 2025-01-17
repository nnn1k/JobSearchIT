import datetime

from pydantic import BaseModel

class GlobalSchema(BaseModel):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
