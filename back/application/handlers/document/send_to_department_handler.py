from application.commands.document.send_to_department import SendToDepartmentCommand
from data.repositories.access_repository import AccessRepository
from data.repositories.document_repository import DocumentRepository
from data.repositories.employee_repository import EmployeeRepository


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

    def handle(self, command: SendToDepartmentCommand):
        # Проверяем право отправителя
        sender_role = self.access_repository.get_user_role_in_department(
            command.sender_user_id,
            command.organization_id,
            command.department_id,
        )
        if not sender_role or not sender_role.can_send_document:
            raise ValueError("У отправителя нет права отправлять документы")

        # Получаем всех сотрудников отдела
        members = self.employee_repository.get_by_department(
            command.organization_id, command.department_id
        )
        if not members:
            raise ValueError("В отделе нет сотрудников")

        results = []
        for member in members:
            # Пропускаем самого отправителя
            if member.user_id == command.sender_user_id:
                continue
            # Пропускаем если уже отправлен
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
