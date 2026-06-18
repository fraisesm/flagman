from pydantic import BaseModel
from typing import Optional


class CreateOrganizationRequest(BaseModel):
    name: str
    owner_id: int


class UpdateOrganizationRequest(BaseModel):
    name: str


class OrganizationResponse(BaseModel):
    id: int
    name: str
    owner_id: int

    class Config:
        from_attributes = True
