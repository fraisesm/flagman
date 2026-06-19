from application.commands.document.send_document import SendDocumentCommand
from data.repositories.access_repository import AccessRepository
from data.repositories.document_repository import DocumentRepository
from data.repositories.employee_repository import EmployeeRepository

BOSS_ROLES = {"boss", "admin", "manager", "director"}


class SendDocumentHandler:
    def __init__(
        self,
        document_repository: DocumentRepository,
        access_repository: AccessRepository,
        employee_repository: EmployeeRepository = None,
    ):
        self.document_repository = document_repository
        self.access_repository = access_repository
        self.employee_repository = employee_repository

    def _sender_can_send(self, command: SendDocumentCommand) -> bool:
        # 1. Check explicit DepartmentRole permission
        sender_role = self.access_repository.get_user_role_in_department(
            command.sender_user_id,
            command.organization_id,
            command.department_id,
        )
        if sender_role and sender_role.can_send_document is True:
            return True

        # 2. Fallback: check EmployeeMembership role (raw ORM model, has .role)
        if self.employee_repository:
            membership = self.employee_repository.get_by_user_and_organization(
                command.sender_user_id,
                command.organization_id,
            )
            if membership and membership.role in BOSS_ROLES:
                return True

        return False

    def handle(self, command: SendDocumentCommand):
        if not self._sender_can_send(command):
            raise ValueError("У отправителя нет права отправлять документы")

        existing = self.document_repository.get_existing_recipient(
            command.document_id,
            command.recipient_user_id,
        )
        if existing:
            raise ValueError("Этот документ уже отправлен данному сотруднику")

        return self.document_repository.send_to_recipient(
            document_id=command.document_id,
            recipient_user_id=command.recipient_user_id,
        )
