from application.commands.document.forward_document import ForwardDocumentCommand
from data.repositories.access_repository import AccessRepository
from data.repositories.document_repository import DocumentRepository
from data.repositories.signature_repository import SignatureRepository


class ForwardDocumentHandler:
    def __init__(
        self,
        document_repository: DocumentRepository,
        access_repository: AccessRepository,
        signature_repository: SignatureRepository,
    ):
        self.document_repository = document_repository
        self.access_repository = access_repository
        self.signature_repository = signature_repository

    def handle(self, command: ForwardDocumentCommand):
        # Получатель должен быть в inbox у отправителя
        incoming = self.document_repository.get_existing_recipient(
            command.document_id, command.sender_user_id
        )
        if not incoming:
            raise ValueError("Документ не найден в вашем входящем")

        # Нельзя перенаправить самому себе
        if command.recipient_user_id == command.sender_user_id:
            raise ValueError("Нельзя перенаправить документ самому себе")

        # Проверяем что не отправляли уже этому получателю
        existing = self.document_repository.get_existing_recipient(
            command.document_id, command.recipient_user_id
        )
        if existing:
            raise ValueError("Документ уже отправлен этому сотруднику")

        recipient = self.document_repository.send_to_recipient(
            document_id=command.document_id,
            recipient_user_id=command.recipient_user_id,
        )
        return recipient
