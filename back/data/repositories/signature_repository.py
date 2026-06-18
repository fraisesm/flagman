from sqlalchemy.orm import Session
from data.models.signature_model import SignatureModel
from data.models.document_recipient_model import DocumentRecipientModel


class SignatureRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, document_id: int, phone_signature: str, confirmation_channel: str = "phone"):
        signature = SignatureModel(
            user_id=user_id,
            document_id=document_id,
            phone_signature=phone_signature,
            confirmation_channel=confirmation_channel,
        )
        self.db.add(signature)

        recipient = (
            self.db.query(DocumentRecipientModel)
            .filter(
                DocumentRecipientModel.document_id == document_id,
                DocumentRecipientModel.recipient_user_id == user_id,
            )
            .first()
        )
        if recipient:
            recipient.status = "signed"

        self.db.commit()
        self.db.refresh(signature)
        return signature

    def get_by_user_and_document(self, user_id: int, document_id: int):
        return (
            self.db.query(SignatureModel)
            .filter(
                SignatureModel.user_id == user_id,
                SignatureModel.document_id == document_id,
            )
            .first()
        )

    def get_by_document(self, document_id: int):
        return self.db.query(SignatureModel).filter(SignatureModel.document_id == document_id).all()
