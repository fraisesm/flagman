from pydantic import BaseModel
from typing import Optional


class CreateDepartmentRequest(BaseModel):
    name: str
    organization_id: int
    description: Optional[str] = None


class UpdateDepartmentRequest(BaseModel):
    name: str
    description: Optional[str] = None


class DepartmentResponse(BaseModel):
    id: int
    name: str
    organization_id: int
    description: Optional[str] = None

    class Config:
        from_attributes = True
