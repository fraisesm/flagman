from application.commands.document.create_document import CreateDocumentCommand
from data.repositories.document_repository import DocumentRepository
from data.models.document_model import DocumentModel


class CreateDocumentHandler:
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    def handle(self, command: CreateDocumentCommand):
        if not command.title:
            raise ValueError("Название документа обязательно")
        if not command.content and not command.link:
            raise ValueError("Необходимо указать текст или ссылку")
        model = DocumentModel(
            title=command.title,
            content=command.content,
            link=command.link,
            sender_user_id=command.sender_user_id,
            organization_id=command.organization_id,
            department_id=command.department_id,
        )
        return self.document_repository.create(model)
