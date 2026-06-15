from application.commands.organization.create_organization import CreateOrganizationCommand
from data.repositories.organization_repository import OrganizationRepository
from domain.organization.organization import Organization


class CreateOrganizationHandler:
    def __init__(self, organization_repository: OrganizationRepository):
        self.organization_repository = organization_repository

    def handle(self, command: CreateOrganizationCommand):
        organization = Organization(
            name=command.name,
            owner_id=command.owner_id,
        )
        return self.organization_repository.create(organization)