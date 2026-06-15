from pydantic import BaseModel


class CreateDepartmentRequest(BaseModel):
    name: str
    organization_id: int
    description: str | None = None