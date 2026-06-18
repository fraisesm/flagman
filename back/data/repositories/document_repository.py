from sqlalchemy.orm import Session
from data.models.document_model import DocumentModel
from data.models.document_recipient_model import DocumentRecipientModel
from domain.document.document import Document


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_document(self, document: Document):
        model = DocumentModel(
            title=document.title,
            content=document.content,
            sender_user_id=document.sender_user_id,
            organization_id=document.organization_id,
            department_id=document.department_id,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def create(self, model: DocumentModel):
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_by_id(self, document_id: int):
        return self.db.query(DocumentModel).filter(DocumentModel.id == document_id).first()

    def get_all_by_sender(self, user_id: int):
        return self.db.query(DocumentModel).filter(DocumentModel.sender_user_id == user_id).all()

    def update(self, document_id: int, title: str, content: str):
        model = self.get_by_id(document_id)
        if model:
            model.title = title
            model.content = content
            self.db.commit()
            self.db.refresh(model)
        return model

    def delete(self, document_id: int):
        model = self.get_by_id(document_id)
        if model:
            self.db.delete(model)
            self.db.commit()
        return model

    def add_recipient(self, recipient: DocumentRecipientModel):
        self.db.add(recipient)
        self.db.commit()
        self.db.refresh(recipient)
        return recipient

    def get_existing_recipient(self, document_id: int, recipient_user_id: int):
        return (
            self.db.query(DocumentRecipientModel)
            .filter(
                DocumentRecipientModel.document_id == document_id,
                DocumentRecipientModel.recipient_user_id == recipient_user_id,
            )
            .first()
        )

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

    def mark_as_read(self, document_id: int, user_id: int):
        """Change status from 'pending' to 'read' when the user opens the document."""
        recipient = (
            self.db.query(DocumentRecipientModel)
            .filter(
                DocumentRecipientModel.document_id == document_id,
                DocumentRecipientModel.recipient_user_id == user_id,
                DocumentRecipientModel.status == "pending",
            )
            .first()
        )
        if recipient:
            recipient.status = "read"
            self.db.commit()
            self.db.refresh(recipient)
        return recipient

    def get_inbox(self, user_id: int):
        return (
            self.db.query(DocumentRecipientModel, DocumentModel)
            .join(DocumentModel, DocumentRecipientModel.document_id == DocumentModel.id)
            .filter(DocumentRecipientModel.recipient_user_id == user_id)
            .all()
        )

    def get_outbox(self, user_id: int):
        return self.db.query(DocumentModel).filter(DocumentModel.sender_user_id == user_id).all()

    def get_pending_inbox(self, user_id: int):
        return (
            self.db.query(DocumentRecipientModel, DocumentModel)
            .join(DocumentModel, DocumentRecipientModel.document_id == DocumentModel.id)
            .filter(
                DocumentRecipientModel.recipient_user_id == user_id,
                DocumentRecipientModel.status == "pending",
            )
            .all()
        )

    def get_read_inbox(self, user_id: int):
        """Documents the user has read but not yet signed."""
        return (
            self.db.query(DocumentRecipientModel, DocumentModel)
            .join(DocumentModel, DocumentRecipientModel.document_id == DocumentModel.id)
            .filter(
                DocumentRecipientModel.recipient_user_id == user_id,
                DocumentRecipientModel.status == "read",
            )
            .all()
        )

    def get_signed_inbox(self, user_id: int):
        """Documents the user has signed."""
        return (
            self.db.query(DocumentRecipientModel, DocumentModel)
            .join(DocumentModel, DocumentRecipientModel.document_id == DocumentModel.id)
            .filter(
                DocumentRecipientModel.recipient_user_id == user_id,
                DocumentRecipientModel.status == "signed",
            )
            .all()
        )

    def get_unread_count(self, user_id: int) -> int:
        """Count of documents with status 'pending' — for the notification badge."""
        return (
            self.db.query(DocumentRecipientModel)
            .filter(
                DocumentRecipientModel.recipient_user_id == user_id,
                DocumentRecipientModel.status == "pending",
            )
            .count()
        )

    def get_document_status_for_user(self, document_id: int, user_id: int):
        return (
            self.db.query(DocumentRecipientModel)
            .filter(
                DocumentRecipientModel.document_id == document_id,
                DocumentRecipientModel.recipient_user_id == user_id,
            )
            .first()
        )
