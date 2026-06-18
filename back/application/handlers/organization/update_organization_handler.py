from application.commands.organization.update_organization import UpdateOrganizationCommand
from data.repositories.organization_repository import OrganizationRepository


class UpdateOrganizationHandler:
    def __init__(self, repository: OrganizationRepository):
        self.repository = repository

    def handle(self, command: UpdateOrganizationCommand):
        org = self.repository.update(command.organization_id, command.name)
        if not org:
            raise ValueError("Организация не найдена")
        return org
