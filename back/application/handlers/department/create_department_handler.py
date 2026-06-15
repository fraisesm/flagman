from application.commands.department.create_department import CreateDepartmentCommand
from data.repositories.department_repository import DepartmentRepository
from domain.employee.department import Department


class CreateDepartmentHandler:
    def __init__(self, department_repository: DepartmentRepository):
        self.department_repository = department_repository

    def handle(self, command: CreateDepartmentCommand):
        department = Department(
            name=command.name,
            organization_id=command.organization_id,
            description=command.description,
        )
        return self.department_repository.create(department)