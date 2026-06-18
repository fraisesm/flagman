class GetOrganizationQuery:
    def __init__(self, organization_id: int):
        self.organization_id = organization_id


class ListOrganizationsQuery:
    def __init__(self, owner_id: int = None, all_organizations: bool = False):
        self.owner_id = owner_id
        self.all_organizations = all_organizations
