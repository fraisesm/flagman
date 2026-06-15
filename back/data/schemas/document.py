from pydantic import BaseModel


class CreateDocumentRequest(BaseModel):
    title: str
    content: str
    sender_user_id: int
    organization_id: int
    department_id: int


class SendDocumentRequest(BaseModel):
    document_id: int
    sender_user_id: int
    organization_id: int
    department_id: int
    recipient_user_id: int

class InboxRequest(BaseModel):
    user_id: int


class OutboxRequest(BaseModel):
    user_id: int