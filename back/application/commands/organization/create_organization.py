class CreateOrganizationCommand:
    def __init__(self, name: str, owner_id: int):
        self.name = name
        self.owner_id = owner_id