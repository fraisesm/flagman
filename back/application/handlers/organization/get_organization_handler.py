from application.queries.organization.get_organization_query import GetOrganizationQuery, ListOrganizationsQuery
from data.repositories.organization_repository import OrganizationRepository


class GetOrganizationHandler:
    def __init__(self, repository: OrganizationRepository):
        self.repository = repository

    def handle(self, query: GetOrganizationQuery):
        org = self.repository.get_by_id(query.organization_id)
        if not org:
            raise ValueError("Организация не найдена")
        return org


class ListOrganizationsHandler:
    def __init__(self, repository: OrganizationRepository):
        self.repository = repository

    def handle(self, query: ListOrganizationsQuery):
        return self.repository.get_all_by_owner(query.owner_id)
