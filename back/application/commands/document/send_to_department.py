class SendToDepartmentCommand:
    def __init__(
        self,
        document_id: int,
        sender_user_id: int,
        organization_id: int,
        department_id: int,
    ):
        self.document_id = document_id
        self.sender_user_id = sender_user_id
        self.organization_id = organization_id
        self.department_id = department_id
