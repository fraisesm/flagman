class CreateDepartmentCommand:
    def __init__(self, name: str, organization_id: int, description: str | None = None):
        self.name = name
        self.organization_id = organization_id
        self.description = description