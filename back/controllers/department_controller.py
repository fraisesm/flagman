from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from application.commands.department.create_department import CreateDepartmentCommand
from application.commands.department.update_department import UpdateDepartmentCommand
from application.handlers.department.create_department_handler import CreateDepartmentHandler
from application.handlers.department.update_department_handler import UpdateDepartmentHandler
from application.handlers.department.get_department_handler import GetDepartmentHandler, ListDepartmentsHandler
from application.queries.department.get_department_query import GetDepartmentQuery, ListDepartmentsQuery
from application.dependencies.auth import get_current_user
from data.db import get_db
from data.repositories.department_repository import DepartmentRepository
from data.schemas.department import CreateDepartmentRequest, UpdateDepartmentRequest, DepartmentResponse

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post("/", response_model=DepartmentResponse)
def create_department(
    request: CreateDepartmentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = DepartmentRepository(db)
    handler = CreateDepartmentHandler(repo)
    command = CreateDepartmentCommand(
        name=request.name,
        organization_id=request.organization_id,
        description=request.description,
    )
    return handler.handle(command)


@router.get("/by-organization/{organization_id}", response_model=List[DepartmentResponse])
def list_departments(organization_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = DepartmentRepository(db)
    return ListDepartmentsHandler(repo).handle(ListDepartmentsQuery(organization_id=organization_id))


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(department_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = DepartmentRepository(db)
    try:
        return GetDepartmentHandler(repo).handle(GetDepartmentQuery(department_id=department_id))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    request: UpdateDepartmentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = DepartmentRepository(db)
    try:
        return UpdateDepartmentHandler(repo).handle(
            UpdateDepartmentCommand(department_id=department_id, name=request.name, description=request.description)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = DepartmentRepository(db)
    result = repo.delete(department_id)
    if not result:
        raise HTTPException(status_code=404, detail="Отдел не найден")
    return {"detail": "Отдел удалён"}
