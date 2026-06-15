from application.commands.document.create_document import CreateDocumentCommand
from data.repositories.document_repository import DocumentRepository
from domain.document.document import Document


class CreateDocumentHandler:
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    def handle(self, command: CreateDocumentCommand):
        document = Document(
            title=command.title,
            content=command.content,
            sender_user_id=command.sender_user_id,
            organization_id=command.organization_id,
            department_id=command.department_id,
        )
        return self.document_repository.create_document(document)