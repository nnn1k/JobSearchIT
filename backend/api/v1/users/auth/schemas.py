from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str


