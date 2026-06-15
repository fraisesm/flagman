from sqlalchemy.orm import Session

from data.models.department_role_model import DepartmentRoleModel
from domain.access.role import DepartmentRole


class AccessRepository:
    def __init__(self, db: Session):
        self.db = db

    def assign_role(self, role: DepartmentRole):
        role_model = DepartmentRoleModel(
            user_id=role.user_id,
            organization_id=role.organization_id,
            department_id=role.department_id,
            role_name=role.role_name,
            can_send_document=role.can_send_document,
            can_sign_document=role.can_sign_document,
            can_manage_department=role.can_manage_department,
        )
        self.db.add(role_model)
        self.db.commit()
        self.db.refresh(role_model)
        return role_model

    def get_user_role_in_department(self, user_id: int, organization_id: int, department_id: int):
        return (
            self.db.query(DepartmentRoleModel)
            .filter(
                DepartmentRoleModel.user_id == user_id,
                DepartmentRoleModel.organization_id == organization_id,
                DepartmentRoleModel.department_id == department_id,
            )
            .first()
        )