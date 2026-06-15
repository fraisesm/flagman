from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from application.commands.employee.invite_employee import InviteEmployeeCommand
from application.handlers.employee.invite_employee_handler import InviteEmployeeHandler
from data.db import get_db
from data.repositories.employee_repository import EmployeeRepository
from data.schemas.employee import InviteEmployeeRequest

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/invite")
def invite_employee(request: InviteEmployeeRequest, db: Session = Depends(get_db)):
    employee_repository = EmployeeRepository(db)
    handler = InviteEmployeeHandler(employee_repository)

    command = InviteEmployeeCommand(
        user_id=request.user_id,
        organization_id=request.organization_id,
        department_id=request.department_id,
        role=request.role,
    )

    try:
        membership = handler.handle(command)
        return {
            "id": membership.id,  # type: ignore
            "user_id": membership.user_id,  # type: ignore
            "organization_id": membership.organization_id,  # type: ignore
            "department_id": membership.department_id,  # type: ignore
            "role": membership.role,  # type: ignore
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))