class SignDocumentCommand:
    def __init__(
        self,
        document_id: int,
        user_id: int,
        organization_id: int,
        department_id: int,
        confirmation_channel: str,
    ):
        self.document_id = document_id
        self.user_id = user_id
        self.organization_id = organization_id
        self.department_id = department_id
        self.confirmation_channel = confirmation_channel