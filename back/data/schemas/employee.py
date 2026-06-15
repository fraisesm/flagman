from pydantic import BaseModel


class InviteEmployeeRequest(BaseModel):
    user_id: int
    organization_id: int
    department_id: int | None = None
    role: str | None = None