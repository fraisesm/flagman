class AssignRoleCommand:
    def __init__(
        self,
        user_id: int,
        organization_id: int,
        department_id: int,
        role_name: str,
        can_send_document: bool = False,
        can_sign_document: bool = False,
        can_manage_department: bool = False,
    ):
        self.user_id = user_id
        self.organization_id = organization_id
        self.department_id = department_id
        self.role_name = role_name
        self.can_send_document = can_send_document
        self.can_sign_document = can_sign_document
        self.can_manage_department = can_manage_department