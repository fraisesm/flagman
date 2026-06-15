class InviteEmployeeCommand:
    def __init__(
        self,
        user_id: int,
        organization_id: int,
        department_id: int | None = None,
        role: str | None = None,
    ):
        self.user_id = user_id
        self.organization_id = organization_id
        self.department_id = department_id
        self.role = role