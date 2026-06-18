from pydantic import BaseModel
from typing import Optional


class InviteEmployeeRequest(BaseModel):
    user_id: int
    organization_id: int
    department_id: Optional[int] = None
    role: str = "employee"


class UpdateEmployeeRequest(BaseModel):
    role: str
    department_id: Optional[int] = None


class EmployeeResponse(BaseModel):
    id: int
    user_id: int
    organization_id: int
    department_id: Optional[int] = None
    role: str

    class Config:
        from_attributes = True
