from sqlalchemy import Column, ForeignKey, Integer, String

from data.db import Base


class DocumentRecipientModel(Base):
    __tablename__ = "document_recipients"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    recipient_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="pending")