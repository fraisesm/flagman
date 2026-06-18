from pydantic import BaseModel


class SignDocumentRequest(BaseModel):
    document_id: int


class SignatureResponse(BaseModel):
    id: int
    user_id: int
    document_id: int
    phone_signature: str

    class Config:
        from_attributes = True
