from application.commands.document.send_document import SendDocumentCommand
from data.repositories.access_repository import AccessRepository
from data.repositories.document_repository import DocumentRepository


class SendDocumentHandler:
    def __init__(
        self,
        document_repository: DocumentRepository,
        access_repository: AccessRepository,
    ):
        self.document_repository = document_repository
        self.access_repository = access_repository

    def handle(self, command: SendDocumentCommand):
        sender_role = self.access_repository.get_user_role_in_department(
            command.sender_user_id,
            command.organization_id,
            command.department_id,
        )

        if not sender_role:
            raise ValueError("У отправителя нет роли в этом отделе")

        if sender_role.can_send_document is not True:  # type: ignore
            raise ValueError("У сотрудника нет права отправлять документы")

        existing_recipient = self.document_repository.get_existing_recipient(
            command.document_id,
            command.recipient_user_id,
        )

        if existing_recipient:
            raise ValueError("Этот документ уже отправлен данному сотруднику")
        
        return self.document_repository.send_to_recipient(
            document_id=command.document_id,
            recipient_user_id=command.recipient_user_id,
        )