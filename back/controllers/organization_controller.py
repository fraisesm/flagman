from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from application.commands.organization.create_organization import CreateOrganizationCommand
from application.handlers.organization.create_organization_handler import CreateOrganizationHandler
from data.db import get_db
from data.repositories.organization_repository import OrganizationRepository
from data.schemas.organization import CreateOrganizationRequest

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/")
def create_organization(request: CreateOrganizationRequest, db: Session = Depends(get_db)):
    organization_repository = OrganizationRepository(db)
    handler = CreateOrganizationHandler(organization_repository)

    command = CreateOrganizationCommand(
        name=request.name,
        owner_id=request.owner_id,
    )

    organization = handler.handle(command)

    return {
        "id": organization.id,  # type: ignore
        "name": organization.name,  # type: ignore
        "owner_id": organization.owner_id,  # type: ignore
    }