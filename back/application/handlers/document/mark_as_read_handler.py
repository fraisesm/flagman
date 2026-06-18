from data.repositories.document_repository import DocumentRepository


class MarkAsReadHandler:
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    def handle(self, document_id: int, user_id: int):
        recipient = self.document_repository.mark_as_read(document_id, user_id)
        if recipient is None:
            # Already read or signed — not an error, just a no-op
            return {"detail": "Документ уже прочитан или подписан"}
        return {"detail": "Статус обновлён: прочитано"}
