from sqlalchemy import Column, ForeignKey, Integer, String, Text

from data.db import Base


class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    link = Column(String, nullable=True)
    sender_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
