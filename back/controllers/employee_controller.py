from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from application.commands.employee.invite_employee import InviteEmployeeCommand
from application.handlers.employee.invite_employee_handler import InviteEmployeeHandler
from application.dependencies.auth import get_current_user
from data.db import get_db
from data.repositories.employee_repository import EmployeeRepository
from data.schemas.employee import InviteEmployeeRequest, UpdateEmployeeRequest, EmployeeResponse

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/invite", response_model=EmployeeResponse)
def invite_employee(
    request: InviteEmployeeRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = EmployeeRepository(db)
    handler = InviteEmployeeHandler(repo)
    command = InviteEmployeeCommand(
        user_id=request.user_id,
        organization_id=request.organization_id,
        department_id=request.department_id,
        role=request.role,
    )
    try:
        return handler.handle(command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/by-organization/{organization_id}", response_model=List[EmployeeResponse])
def list_employees(organization_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = EmployeeRepository(db)
    return repo.get_all_by_organization(organization_id)


# Front-end uses GET /employees/list/{dept_id} to populate recipient dropdown
@router.get("/list/{department_id}", response_model=List[EmployeeResponse])
def list_employees_by_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Returns all employees of a specific department (used by boss to pick a recipient)."""
    repo = EmployeeRepository(db)
    # get_by_department requires org_id too; fall back to filtering all by dept only
    from data.models.employee_membership_model import EmployeeMembershipModel
    from data.models.user_model import UserModel
    results = (
        db.query(EmployeeMembershipModel)
        .filter(EmployeeMembershipModel.department_id == department_id)
        .all()
    )
    enriched = [repo._enrich(m) for m in results]
    return enriched


@router.get("/{membership_id}", response_model=EmployeeResponse)
def get_employee(membership_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = EmployeeRepository(db)
    result = repo.get_by_id(membership_id)
    if not result:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return result


@router.put("/{membership_id}", response_model=EmployeeResponse)
def update_employee(
    membership_id: int,
    request: UpdateEmployeeRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = EmployeeRepository(db)
    result = repo.update_role(membership_id, request.role, request.department_id)
    if not result:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return result


@router.delete("/{membership_id}")
def remove_employee(membership_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = EmployeeRepository(db)
    result = repo.delete(membership_id)
    if not result:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return {"detail": "Сотрудник удалён из организации"}
