from pydantic import BaseModel


class AssignRoleRequest(BaseModel):
    user_id: int
    organization_id: int
    department_id: int
    role_name: str
    can_send_document: bool = False
    can_sign_document: bool = False
    can_manage_department: bool = False


class UpdateRoleRequest(BaseModel):
    role_name: str
    can_send_document: bool = False
    can_sign_document: bool = False
    can_manage_department: bool = False


class AccessResponse(BaseModel):
    id: int
    user_id: int
    organization_id: int
    department_id: int
    role_name: str
    can_send_document: bool
    can_sign_document: bool
    can_manage_department: bool

    class Config:
        from_attributes = True
