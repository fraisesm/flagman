from data.repositories.document_repository import DocumentRepository


class GetReadInboxHandler:
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    def handle(self, user_id: int):
        return self.document_repository.get_read_inbox(user_id)
