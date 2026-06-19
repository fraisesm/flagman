from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str
    role: Optional[str] = "employee"


class RegisterResponse(BaseModel):
    message: str
    id: int


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: str


class UserMeResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    role: str

    class Config:
        from_attributes = True
