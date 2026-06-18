from sqlalchemy.orm import Session
from data.models.employee_membership_model import EmployeeMembershipModel
from domain.employee.employee_membership import EmployeeMembership


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_membership(self, membership: EmployeeMembership):
        model = EmployeeMembershipModel(
            user_id=membership.user_id,
            organization_id=membership.organization_id,
            department_id=membership.department_id,
            role=membership.role,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_by_user_and_organization(self, user_id: int, organization_id: int):
        return (
            self.db.query(EmployeeMembershipModel)
            .filter(
                EmployeeMembershipModel.user_id == user_id,
                EmployeeMembershipModel.organization_id == organization_id,
            )
            .first()
        )

    def get_by_id(self, membership_id: int):
        return self.db.query(EmployeeMembershipModel).filter(EmployeeMembershipModel.id == membership_id).first()

    def get_all_by_organization(self, organization_id: int):
        return self.db.query(EmployeeMembershipModel).filter(EmployeeMembershipModel.organization_id == organization_id).all()

    def update_role(self, membership_id: int, role: str, department_id: int):
        model = self.get_by_id(membership_id)
        if model:
            model.role = role
            model.department_id = department_id
            self.db.commit()
            self.db.refresh(model)
        return model

    def delete(self, membership_id: int):
        model = self.get_by_id(membership_id)
        if model:
            self.db.delete(model)
            self.db.commit()
        return model
