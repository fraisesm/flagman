from application.commands.department.update_department import UpdateDepartmentCommand
from data.repositories.department_repository import DepartmentRepository


class UpdateDepartmentHandler:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository

    def handle(self, command: UpdateDepartmentCommand):
        dept = self.repository.update(command.department_id, command.name, command.description)
        if not dept:
            raise ValueError("Отдел не найден")
        return dept
