from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from application.commands.access.assign_role import AssignRoleCommand
from application.handlers.access.assign_role_handler import AssignRoleHandler
from application.dependencies.auth import get_current_user
from application.dependencies.roles import require_admin
from data.db import get_db
from data.repositories.access_repository import AccessRepository
from data.schemas.access import AssignRoleRequest, UpdateRoleRequest, AccessResponse

router = APIRouter(prefix="/access", tags=["Access"])


@router.post("/assign-role", response_model=AccessResponse)
def assign_role(
    request: AssignRoleRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),   # ← только admin
):
    repo = AccessRepository(db)
    handler = AssignRoleHandler(repo)
    command = AssignRoleCommand(
        user_id=request.user_id,
        organization_id=request.organization_id,
        department_id=request.department_id,
        role_name=request.role_name,
        can_send_document=request.can_send_document,
        can_sign_document=request.can_sign_document,
        can_manage_department=request.can_manage_department,
    )
    try:
        return handler.handle(command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/by-organization/{organization_id}", response_model=List[AccessResponse])
def list_roles(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),   # ← только admin
):
    repo = AccessRepository(db)
    return repo.get_all_by_organization(organization_id)


@router.get("/{role_id}", response_model=AccessResponse)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    repo = AccessRepository(db)
    result = repo.get_by_id(role_id)
    if not result:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    return result


@router.put("/{role_id}", response_model=AccessResponse)
def update_role(
    role_id: int,
    request: UpdateRoleRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),   # ← только admin
):
    repo = AccessRepository(db)
    result = repo.update(role_id, request.role_name, request.can_send_document, request.can_sign_document, request.can_manage_department)
    if not result:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    return result


@router.delete("/{role_id}")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),   # ← только admin
):
    repo = AccessRepository(db)
    result = repo.delete(role_id)
    if not result:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    return {"detail": "Роль удалена"}
