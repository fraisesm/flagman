from sqlalchemy.orm import Session
from data.models.employee_membership_model import EmployeeMembershipModel
from data.models.user_model import UserModel
from domain.employee.employee_membership import EmployeeMembership


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def _enrich(self, membership):
        """Return a plain dict with user fields merged in so Pydantic can serialise them."""
        if membership is None:
            return None
        user = self.db.query(UserModel).filter(UserModel.id == membership.user_id).first()
        return {
            "id":              membership.id,
            "user_id":         membership.user_id,
            "organization_id": membership.organization_id,
            "department_id":   membership.department_id,
            "role":            membership.role,
            "full_name":       user.full_name if user else None,
            "email":           user.email     if user else None,
        }

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
        return self._enrich(model)

    def get_by_user_and_organization(self, user_id: int, organization_id: int):
        """Returns raw ORM model (needed by send_document_handler role check)."""
        return (
            self.db.query(EmployeeMembershipModel)
            .filter(
                EmployeeMembershipModel.user_id == user_id,
                EmployeeMembershipModel.organization_id == organization_id,
            )
            .first()
        )

    def get_by_id(self, membership_id: int):
        result = self.db.query(EmployeeMembershipModel).filter(EmployeeMembershipModel.id == membership_id).first()
        return self._enrich(result)

    def get_all_by_organization(self, organization_id: int):
        results = (
            self.db.query(EmployeeMembershipModel)
            .filter(EmployeeMembershipModel.organization_id == organization_id)
            .all()
        )
        return [self._enrich(m) for m in results]

    def get_by_department(self, organization_id: int, department_id: int):
        results = (
            self.db.query(EmployeeMembershipModel)
            .filter(
                EmployeeMembershipModel.organization_id == organization_id,
                EmployeeMembershipModel.department_id == department_id,
            )
            .all()
        )
        return [self._enrich(m) for m in results]

    def get_by_department_only(self, department_id: int):
        """Used by /employees/list/{department_id} — filter by department only."""
        results = (
            self.db.query(EmployeeMembershipModel)
            .filter(EmployeeMembershipModel.department_id == department_id)
            .all()
        )
        return [self._enrich(m) for m in results]

    def update_role(self, membership_id: int, role: str, department_id: int):
        model = self.db.query(EmployeeMembershipModel).filter(EmployeeMembershipModel.id == membership_id).first()
        if model:
            model.role = role
            model.department_id = department_id
            self.db.commit()
            self.db.refresh(model)
        return self._enrich(model)

    def delete(self, membership_id: int):
        model = self.db.query(EmployeeMembershipModel).filter(EmployeeMembershipModel.id == membership_id).first()
        if model:
            self.db.delete(model)
            self.db.commit()
        return model
