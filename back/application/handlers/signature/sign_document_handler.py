import hmac
import hashlib
from data.repositories.signature_repository import SignatureRepository
from data.repositories.document_repository import DocumentRepository
from data.repositories.user_repository import UserRepository
from data.models.signature_model import SignatureModel


class SignDocumentHandler:
    def __init__(
        self,
        signature_repository: SignatureRepository,
        document_repository: DocumentRepository,
        user_repository: UserRepository,
    ):
        self.signature_repository = signature_repository
        self.document_repository = document_repository
        self.user_repository = user_repository

    def handle(self, user_id: int, document_id: int) -> SignatureModel:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")

        document = self.document_repository.get_by_id(document_id)
        if not document:
            raise ValueError("Документ не найден")

        existing = self.signature_repository.get_by_user_and_document(user_id, document_id)
        if existing:
            raise ValueError("Документ уже подписан")

        phone_signature = hmac.new(
            key=user.phone.encode(),
            msg=str(document_id).encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()

        return self.signature_repository.create(user_id, document_id, phone_signature)
