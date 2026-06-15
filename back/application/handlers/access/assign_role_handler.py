from application.commands.access.assign_role import AssignRoleCommand
from data.repositories.access_repository import AccessRepository
from domain.access.role import DepartmentRole


class AssignRoleHandler:
    def __init__(self, access_repository: AccessRepository):
        self.access_repository = access_repository

    def handle(self, command: AssignRoleCommand):
        existing_role = self.access_repository.get_user_role_in_department(
            command.user_id,
            command.organization_id,
            command.department_id,
        )
        if existing_role:
            raise ValueError("Роль для сотрудника в этом отделе уже назначена")

        role = DepartmentRole(
            user_id=command.user_id,
            organization_id=command.organization_id,
            department_id=command.department_id,
            role_name=command.role_name,
            can_send_document=command.can_send_document,
            can_sign_document=command.can_sign_document,
            can_manage_department=command.can_manage_department,
        )
        return self.access_repository.assign_role(role)