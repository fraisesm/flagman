from sqlalchemy.orm import Session
from data.models.department_model import DepartmentModel
from domain.employee.department import Department


class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, department: Department):
        model = DepartmentModel(
            name=department.name,
            organization_id=department.organization_id,
            description=department.description,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_by_id(self, department_id: int):
        return self.db.query(DepartmentModel).filter(DepartmentModel.id == department_id).first()

    def get_all_by_organization(self, organization_id: int):
        return self.db.query(DepartmentModel).filter(DepartmentModel.organization_id == organization_id).all()

    def update(self, department_id: int, name: str, description: str):
        model = self.get_by_id(department_id)
        if model:
            model.name = name
            model.description = description
            self.db.commit()
            self.db.refresh(model)
        return model

    def delete(self, department_id: int):
        model = self.get_by_id(department_id)
        if model:
            self.db.delete(model)
            self.db.commit()
        return model
