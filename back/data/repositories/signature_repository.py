from sqlalchemy.orm import Session

from data.models.signature_model import SignatureModel
from data.models.document_recipient_model import DocumentRecipientModel
from data.models.user_model import UserModel
from domain.signature.signature import Signature


class SignatureRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int):
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_document_recipient(self, document_id: int, user_id: int):
        return (
            self.db.query(DocumentRecipientModel)
            .filter(
                DocumentRecipientModel.document_id == document_id,
                DocumentRecipientModel.recipient_user_id == user_id,
            )
            .first()
        )

    def create_signature(self, signature: Signature):
        signature_model = SignatureModel(
            document_id=signature.document_id,
            user_id=signature.user_id,
            phone_signature=signature.phone_signature,
            confirmation_channel=signature.confirmation_channel,
        )
        self.db.add(signature_model)
        self.db.commit()
        self.db.refresh(signature_model)
        return signature_model

    def mark_document_as_signed(self, document_id: int, user_id: int):
        recipient = self.get_document_recipient(document_id, user_id)
        if recipient:
            recipient.status = "signed" # type: ignore
            self.db.commit()
            self.db.refresh(recipient)
        return recipient