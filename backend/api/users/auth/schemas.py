from pydantic import BaseModel, EmailStr
from enum import Enum

class UserType(str, Enum):
    worker: str = "workers"
    employer: str = "employers"

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
