class UpdateOrganizationCommand:
    def __init__(self, organization_id: int, name: str):
        self.organization_id = organization_id
        self.name = name
