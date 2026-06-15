from sqlalchemy import Column, ForeignKey, Integer, String

from data.db import Base


class SignatureModel(Base):
    __tablename__ = "signatures"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    phone_signature = Column(String, nullable=False)
    confirmation_channel = Column(String, nullable=False)