from sqlalchemy.orm import Session

from data.models.document_model import DocumentModel
from data.models.document_recipient_model import DocumentRecipientModel
from domain.document.document import Document
from data.models.signature_model import SignatureModel

class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_document(self, document: Document):
        document_model = DocumentModel(
            title=document.title,
            content=document.content,
            sender_user_id=document.sender_user_id,
            organization_id=document.organization_id,
            department_id=document.department_id,
        )
        self.db.add(document_model)
        self.db.commit()
        self.db.refresh(document_model)
        return document_model
    

    def send_to_recipient(self, document_id: int, recipient_user_id: int):
        recipient = DocumentRecipientModel(
            document_id=document_id,
            recipient_user_id=recipient_user_id,
            status="pending",
        )
        self.db.add(recipient)
        self.db.commit()
        self.db.refresh(recipient)
        return recipient
    
    def get_outbox(self, sender_user_id: int):
        return (
            self.db.query(DocumentModel)
            .filter(DocumentModel.sender_user_id == sender_user_id)
            .all()
        )

    def get_inbox(self, recipient_user_id: int):
        return (
            self.db.query(DocumentRecipientModel, DocumentModel)
            .join(
                DocumentModel,
                DocumentRecipientModel.document_id == DocumentModel.id,
            )
            .filter(DocumentRecipientModel.recipient_user_id == recipient_user_id)
            .all()
        )

    def get_document_status_for_user(self, document_id: int, recipient_user_id: int):
        recipient = (
            self.db.query(DocumentRecipientModel)
            .filter(
                DocumentRecipientModel.document_id == document_id,
                DocumentRecipientModel.recipient_user_id == recipient_user_id,
            )
            .first()
        )

        if not recipient:
            return None

        signature = (
            self.db.query(SignatureModel)
            .filter(
                SignatureModel.document_id == document_id,
                SignatureModel.signer_user_id == recipient_user_id,
            )
            .first()
        )

        return {
            "document_id": recipient.document_id,
            "recipient_user_id": recipient.recipient_user_id,
            "status": recipient.status,
            "signature_id": signature.id if signature else None,  # type: ignore
            "signed": signature is not None,
        }
    
    def get_pending_inbox(self, recipient_user_id: int):
        return (
            self.db.query(DocumentRecipientModel, DocumentModel)
            .join(
                DocumentModel,
                DocumentRecipientModel.document_id == DocumentModel.id,
            )
            .filter(
                DocumentRecipientModel.recipient_user_id == recipient_user_id,
                DocumentRecipientModel.status == "pending",
            )
            .all()
        )
    
    def get_existing_recipient(self, document_id: int, recipient_user_id: int):
        return (
            self.db.query(DocumentRecipientModel)
            .filter(
                DocumentRecipientModel.document_id == document_id,
                DocumentRecipientModel.recipient_user_id == recipient_user_id,
            )
            .first()
        )