from pydantic import BaseModel


class SignDocumentRequest(BaseModel):
    document_id: int
    user_id: int
    organization_id: int
    department_id: int
    confirmation_channel: str