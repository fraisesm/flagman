from pydantic import BaseModel
from typing import Optional, List


class CreateDocumentRequest(BaseModel):
    title: str
    content: str
    organization_id: int
    department_id: Optional[int] = None


class UpdateDocumentRequest(BaseModel):
    title: str
    content: str


class SendDocumentRequest(BaseModel):
    document_id: int
    organization_id: int
    department_id: Optional[int] = None
    recipient_user_id: int


class SendToDepartmentRequest(BaseModel):
    document_id: int
    organization_id: int
    department_id: int


class ForwardDocumentRequest(BaseModel):
    document_id: int
    organization_id: int
    department_id: Optional[int] = None
    recipient_user_id: int


class InboxRequest(BaseModel):
    user_id: int


class OutboxRequest(BaseModel):
    user_id: int


class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    sender_user_id: int
    organization_id: int
    department_id: Optional[int] = None

    class Config:
        from_attributes = True
