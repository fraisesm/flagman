from sqlalchemy.orm import Session
from data.models.document_model import DocumentModel
from data.models.document_recipient_model import DocumentRecipientModel


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

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

    def get_document_status_for_user(self, document_id: int, user_id: int):
        return (
            self.db.query(DocumentRecipientModel)
            .filter(
                DocumentRecipientModel.document_id == document_id,
                DocumentRecipientModel.recipient_user_id == user_id,
            )
            .first()
        )
