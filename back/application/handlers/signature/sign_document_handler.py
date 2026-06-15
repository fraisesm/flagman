from application.commands.signature.sign_document import SignDocumentCommand
from data.repositories.access_repository import AccessRepository
from data.repositories.signature_repository import SignatureRepository
from domain.signature.signature import Signature


class SignDocumentHandler:
    def __init__(
        self,
        signature_repository: SignatureRepository,
        access_repository: AccessRepository,
    ):
        self.signature_repository = signature_repository
        self.access_repository = access_repository

    def handle(self, command: SignDocumentCommand):
        user_role = self.access_repository.get_user_role_in_department(
            command.user_id,
            command.organization_id,
            command.department_id,
        )

        if not user_role:
            raise ValueError("У сотрудника нет роли в этом отделе")

        if user_role.can_sign_document is not True:  # type: ignore
            raise ValueError("У сотрудника нет права подписывать документы")

        recipient = self.signature_repository.get_document_recipient(
            command.document_id,
            command.user_id,
        )
        if not recipient:
            raise ValueError("Документ не назначен этому сотруднику")

        user = self.signature_repository.get_user_by_id(command.user_id)
        if not user:
            raise ValueError("Сотрудник не найден")

        phone_signature = f"SIGN-{user.phone[-4:]}-{command.document_id}"  # type: ignore

        signature = Signature(
            document_id=command.document_id,
            user_id=command.user_id,
            phone_signature=phone_signature,
            confirmation_channel=command.confirmation_channel,
        )

        created_signature = self.signature_repository.create_signature(signature)
        self.signature_repository.mark_document_as_signed(
            command.document_id,
            command.user_id,
        )

        return created_signature