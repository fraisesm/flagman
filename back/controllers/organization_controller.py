from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from application.commands.organization.create_organization import CreateOrganizationCommand
from application.commands.organization.update_organization import UpdateOrganizationCommand
from application.handlers.organization.create_organization_handler import CreateOrganizationHandler
from application.handlers.organization.update_organization_handler import UpdateOrganizationHandler
from application.handlers.organization.get_organization_handler import GetOrganizationHandler, ListOrganizationsHandler
from application.queries.organization.get_organization_query import GetOrganizationQuery, ListOrganizationsQuery
from application.dependencies.auth import get_current_user
from data.db import get_db
from data.repositories.organization_repository import OrganizationRepository
from data.schemas.organization import CreateOrganizationRequest, UpdateOrganizationRequest, OrganizationResponse
from typing import List

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/", response_model=OrganizationResponse)
def create_organization(
    request: CreateOrganizationRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = OrganizationRepository(db)
    handler = CreateOrganizationHandler(repo)
    command = CreateOrganizationCommand(name=request.name, owner_id=current_user.id)
    return handler.handle(command)


@router.get("/", response_model=List[OrganizationResponse])
def list_organizations(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = OrganizationRepository(db)
    handler = ListOrganizationsHandler(repo)
    # Админ видит только свои организации (где он owner).
    # Начальник и сотрудник видят все организации — чтобы выбрать свою.
    if current_user.role == "admin":
        query = ListOrganizationsQuery(owner_id=current_user.id, all_organizations=False)
    else:
        query = ListOrganizationsQuery(all_organizations=True)
    return handler.handle(query)


@router.get("/{organization_id}", response_model=OrganizationResponse)
def get_organization(organization_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = OrganizationRepository(db)
    handler = GetOrganizationHandler(repo)
    try:
        return handler.handle(GetOrganizationQuery(organization_id=organization_id))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{organization_id}", response_model=OrganizationResponse)
def update_organization(
    organization_id: int,
    request: UpdateOrganizationRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = OrganizationRepository(db)
    handler = UpdateOrganizationHandler(repo)
    try:
        return handler.handle(UpdateOrganizationCommand(organization_id=organization_id, name=request.name))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{organization_id}")
def delete_organization(organization_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = OrganizationRepository(db)
    result = repo.delete(organization_id)
    if not result:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return {"detail": "Организация удалена"}
