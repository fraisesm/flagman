from sqlalchemy.orm import Session

from data.models.employee_membership_model import EmployeeMembershipModel
from domain.employee.employee_membership import EmployeeMembership


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_membership(self, membership: EmployeeMembership):
        membership_model = EmployeeMembershipModel(
            user_id=membership.user_id,
            organization_id=membership.organization_id,
            department_id=membership.department_id,
            role=membership.role,
        )
        self.db.add(membership_model)
        self.db.commit()
        self.db.refresh(membership_model)
        return membership_model

    def get_by_user_and_organization(self, user_id: int, organization_id: int):
        return (
            self.db.query(EmployeeMembershipModel)
            .filter(
                EmployeeMembershipModel.user_id == user_id,
                EmployeeMembershipModel.organization_id == organization_id,
            )
            .first()
        )