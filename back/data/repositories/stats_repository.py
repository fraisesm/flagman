from sqlalchemy.orm import Session
from sqlalchemy import func
from data.models.document_model import DocumentModel
from data.models.document_recipient_model import DocumentRecipientModel
from data.models.signature_model import SignatureModel
from data.models.user_model import UserModel
from data.models.organization_model import OrganizationModel
from data.models.department_model import DepartmentModel


class StatsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_summary(self) -> dict:
        total_documents = self.db.query(func.count(DocumentModel.id)).scalar()
        total_users = self.db.query(func.count(UserModel.id)).scalar()
        total_organizations = self.db.query(func.count(OrganizationModel.id)).scalar()
        total_departments = self.db.query(func.count(DepartmentModel.id)).scalar()
        total_signatures = self.db.query(func.count(SignatureModel.id)).scalar()

        pending_count = (
            self.db.query(func.count(DocumentRecipientModel.id))
            .filter(DocumentRecipientModel.status == "pending")
            .scalar()
        )
        read_count = (
            self.db.query(func.count(DocumentRecipientModel.id))
            .filter(DocumentRecipientModel.status == "read")
            .scalar()
        )
        signed_count = (
            self.db.query(func.count(DocumentRecipientModel.id))
            .filter(DocumentRecipientModel.status == "signed")
            .scalar()
        )

        users_by_role = (
            self.db.query(UserModel.role, func.count(UserModel.id))
            .group_by(UserModel.role)
            .all()
        )

        return {
            "total_documents": total_documents,
            "total_users": total_users,
            "total_organizations": total_organizations,
            "total_departments": total_departments,
            "total_signatures": total_signatures,
            "documents_by_status": {
                "pending": pending_count,
                "read": read_count,
                "signed": signed_count,
            },
            "users_by_role": {
                role: count for role, count in users_by_role
            },
        }

    def get_all_documents(self):
        """All documents with sender info for admin view."""
        return self.db.query(DocumentModel).order_by(DocumentModel.id.desc()).all()

    def get_recent_signatures(self, limit: int = 20):
        """Most recent signatures across all documents."""
        return (
            self.db.query(SignatureModel)
            .order_by(SignatureModel.id.desc())
            .limit(limit)
            .all()
        )
