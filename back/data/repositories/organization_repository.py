from sqlalchemy.orm import Session

from data.models.organization_model import OrganizationModel
from domain.organization.organization import Organization


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, organization: Organization):
        organization_model = OrganizationModel(
            name=organization.name,
            owner_id=organization.owner_id,
        )
        self.db.add(organization_model)
        self.db.commit()
        self.db.refresh(organization_model)
        return organization_model

    def get_by_id(self, organization_id: int):
        return (
            self.db.query(OrganizationModel)
            .filter(OrganizationModel.id == organization_id)
            .first()
        )