class GetOrganizationQuery:
    def __init__(self, organization_id: int):
        self.organization_id = organization_id


class ListOrganizationsQuery:
    def __init__(self, owner_id: int):
        self.owner_id = owner_id
