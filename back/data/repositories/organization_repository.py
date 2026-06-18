from sqlalchemy.orm import Session
from data.models.organization_model import OrganizationModel
from domain.organization.organization import Organization


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, organization: Organization):
        model = OrganizationModel(name=organization.name, owner_id=organization.owner_id)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_by_id(self, organization_id: int):
        return self.db.query(OrganizationModel).filter(OrganizationModel.id == organization_id).first()

    def get_all_by_owner(self, owner_id: int):
        return self.db.query(OrganizationModel).filter(OrganizationModel.owner_id == owner_id).all()

    def update(self, organization_id: int, name: str):
        model = self.get_by_id(organization_id)
        if model:
            model.name = name
            self.db.commit()
            self.db.refresh(model)
        return model

    def delete(self, organization_id: int):
        model = self.get_by_id(organization_id)
        if model:
            self.db.delete(model)
            self.db.commit()
        return model
