from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from application.commands.department.create_department import CreateDepartmentCommand
from application.handlers.department.create_department_handler import CreateDepartmentHandler
from data.db import get_db
from data.repositories.department_repository import DepartmentRepository
from data.schemas.department import CreateDepartmentRequest

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post("/")
def create_department(request: CreateDepartmentRequest, db: Session = Depends(get_db)):
    department_repository = DepartmentRepository(db)
    handler = CreateDepartmentHandler(department_repository)

    command = CreateDepartmentCommand(
        name=request.name,
        organization_id=request.organization_id,
        description=request.description,
    )

    department = handler.handle(command)

    return {
        "id": department.id,  # type: ignore
        "name": department.name,  # type: ignore
        "organization_id": department.organization_id,  # type: ignore
        "description": department.description,  # type: ignore
    }