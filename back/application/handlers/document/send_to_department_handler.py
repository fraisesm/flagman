from application.commands.document.send_to_department import SendToDepartmentCommand
from data.repositories.access_repository import AccessRepository
from data.repositories.document_repository import DocumentRepository
from data.repositories.employee_repository import EmployeeRepository

BOSS_ROLES = {"boss", "admin", "manager", "director"}


class SendToDepartmentHandler:
    def __init__(
        self,
        document_repository: DocumentRepository,
        access_repository: AccessRepository,
        employee_repository: EmployeeRepository,
    ):
        self.document_repository = document_repository
        self.access_repository = access_repository
        self.employee_repository = employee_repository

    def _sender_can_send(self, command: SendToDepartmentCommand) -> bool:
        # 1. Проверяем DepartmentRoleModel
        sender_role = self.access_repository.get_user_role_in_department(
            command.sender_user_id,
            command.organization_id,
            command.department_id,
        )
        if sender_role and sender_role.can_send_document is True:
            return True

        # 2. Fallback: проверяем роль в EmployeeMembership
        membership = self.employee_repository.get_by_user_and_organization(
            command.sender_user_id,
            command.organization_id,
        )
        if membership and membership.role in BOSS_ROLES:
            return True

        return False

    def handle(self, command: SendToDepartmentCommand):
        if not self._sender_can_send(command):
            raise ValueError("У отправителя нет права отправлять документы")

        members = self.employee_repository.get_by_department(
            command.organization_id, command.department_id
        )
        if not members:
            raise ValueError("В отделе нет сотрудников")

        results = []
        for member in members:
            if member.user_id == command.sender_user_id:
                continue
            existing = self.document_repository.get_existing_recipient(
                command.document_id, member.user_id
            )
            if existing:
                continue
            recipient = self.document_repository.send_to_recipient(
                document_id=command.document_id,
                recipient_user_id=member.user_id,
            )
            results.append(recipient)
        return results
