from sqlalchemy.orm import Session
from data.models.department_role_model import DepartmentRoleModel


class AccessRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, role_model: DepartmentRoleModel):
        self.db.add(role_model)
        self.db.commit()
        self.db.refresh(role_model)
        return role_model

    def get_by_id(self, role_id: int):
        return self.db.query(DepartmentRoleModel).filter(DepartmentRoleModel.id == role_id).first()

    def get_by_user_and_department(self, user_id: int, department_id: int):
        return (
            self.db.query(DepartmentRoleModel)
            .filter(
                DepartmentRoleModel.user_id == user_id,
                DepartmentRoleModel.department_id == department_id,
            )
            .first()
        )

    def get_all_by_organization(self, organization_id: int):
        return (
            self.db.query(DepartmentRoleModel)
            .filter(DepartmentRoleModel.organization_id == organization_id)
            .all()
        )

    def update(self, role_id: int, role_name: str, can_send: bool, can_sign: bool, can_manage: bool):
        model = self.get_by_id(role_id)
        if model:
            model.role_name = role_name
            model.can_send_document = can_send
            model.can_sign_document = can_sign
            model.can_manage_department = can_manage
            self.db.commit()
            self.db.refresh(model)
        return model

    def delete(self, role_id: int):
        model = self.get_by_id(role_id)
        if model:
            self.db.delete(model)
            self.db.commit()
        return model

    def can_sign(self, user_id: int, organization_id: int):
        return (
            self.db.query(DepartmentRoleModel)
            .filter(
                DepartmentRoleModel.user_id == user_id,
                DepartmentRoleModel.organization_id == organization_id,
                DepartmentRoleModel.can_sign_document == True,
            )
            .first()
        )

    def can_send(self, user_id: int, organization_id: int):
        return (
            self.db.query(DepartmentRoleModel)
            .filter(
                DepartmentRoleModel.user_id == user_id,
                DepartmentRoleModel.organization_id == organization_id,
                DepartmentRoleModel.can_send_document == True,
            )
            .first()
        )
