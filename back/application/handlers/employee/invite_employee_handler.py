from application.commands.employee.invite_employee import InviteEmployeeCommand
from data.repositories.employee_repository import EmployeeRepository
from domain.employee.employee_membership import EmployeeMembership


class InviteEmployeeHandler:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def handle(self, command: InviteEmployeeCommand):
        existing_membership = self.employee_repository.get_by_user_and_organization(
            command.user_id,
            command.organization_id,
        )
        if existing_membership:
            raise ValueError("Сотрудник уже добавлен в организацию")

        membership = EmployeeMembership(
            user_id=command.user_id,
            organization_id=command.organization_id,
            department_id=command.department_id,
            role=command.role,
        )

        return self.employee_repository.create_membership(membership)