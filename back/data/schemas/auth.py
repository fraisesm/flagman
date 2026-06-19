import re
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, field_validator

# Принимаем: +79891234567 / 79891234567 / 89891234567
PHONE_REGEX = re.compile(r'^(\+7|7|8)\d{10}$')


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str
    role: Optional[Literal["admin", "boss", "employee"]] = "employee"

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v.strip()) < 6:
            raise ValueError("Пароль должен содержать минимум 6 символов")
        return v

    @field_validator("full_name")
    @classmethod
    def full_name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Имя не может быть пустым")
        return v.strip()

    @field_validator("phone")
    @classmethod
    def phone_valid(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Телефон не может быть пустым")
        cleaned = re.sub(r'[\s\-()]', '', v)
        if not PHONE_REGEX.match(cleaned):
            raise ValueError(
                "Неверный формат номера телефона. "
                "Используйте формат +79891234567, 79891234567 или 89891234567"
            )
        if cleaned.startswith('8'):
            cleaned = '+7' + cleaned[1:]
        elif cleaned.startswith('7'):
            cleaned = '+' + cleaned
        return cleaned


class RegisterResponse(BaseModel):
    message: str
    id: Optional[int] = None  # user id — needed by front-end to set lastIds.user_id


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Пароль не может быть пустым")
        return v


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    full_name: str
    email: str
    role: str


class UserMeResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    role: str

    class Config:
        from_attributes = True
