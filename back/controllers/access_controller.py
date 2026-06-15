from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from application.commands.access.assign_role import AssignRoleCommand
from application.handlers.access.assign_role_handler import AssignRoleHandler
from data.db import get_db
from data.repositories.access_repository import AccessRepository
from data.schemas.access import AssignRoleRequest

router = APIRouter(prefix="/access", tags=["Access"])


@router.post("/assign-role")
def assign_role(request: AssignRoleRequest, db: Session = Depends(get_db)):
    repository = AccessRepository(db)
    handler = AssignRoleHandler(repository)

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
        role = handler.handle(command)
        return {
            "id": role.id,  # type: ignore
            "user_id": role.user_id,  # type: ignore
            "organization_id": role.organization_id,  # type: ignore
            "department_id": role.department_id,  # type: ignore
            "role_name": role.role_name,  # type: ignore
            "can_send_document": role.can_send_document,  # type: ignore
            "can_sign_document": role.can_sign_document,  # type: ignore
            "can_manage_department": role.can_manage_department,  # type: ignore
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))