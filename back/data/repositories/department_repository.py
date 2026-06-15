from sqlalchemy.orm import Session

from data.models.department_model import DepartmentModel
from domain.employee.department import Department


class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, department: Department):
        department_model = DepartmentModel(
            name=department.name,
            organization_id=department.organization_id,
            description=department.description,
        )
        self.db.add(department_model)
        self.db.commit()
        self.db.refresh(department_model)
        return department_model

    def get_by_id(self, department_id: int):
        return (
            self.db.query(DepartmentModel)
            .filter(DepartmentModel.id == department_id)
            .first()
        )