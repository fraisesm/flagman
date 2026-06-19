from pydantic import BaseModel, HttpUrl
from typing import Optional


class CreateDocumentRequest(BaseModel):
    title: str
    content: Optional[str] = None
    link: Optional[str] = None          # optional URL
    organization_id: int
    department_id: Optional[int] = None


class UpdateDocumentRequest(BaseModel):
    title: str
    content: Optional[str] = None
    link: Optional[str] = None


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
    content: Optional[str] = None
    link: Optional[str] = None
    sender_user_id: int
    organization_id: int
    department_id: Optional[int] = None

    class Config:
        from_attributes = True
