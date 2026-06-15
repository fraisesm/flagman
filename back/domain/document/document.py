class Document:
    def __init__(
        self,
        title: str,
        content: str,
        sender_user_id: int,
        organization_id: int,
        department_id: int,
    ):
        self.title = title
        self.content = content
        self.sender_user_id = sender_user_id
        self.organization_id = organization_id
        self.department_id = department_id