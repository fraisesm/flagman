from fastapi import FastAPI

from controllers.auth_controller import router as auth_router
from controllers.organization_controller import router as organization_router
from controllers.department_controller import router as department_router
from controllers.employee_controller import router as employee_router
from controllers.access_controller import router as access_router
from controllers.document_controller import router as document_router
from controllers.signature_controller import router as signature_router

from data.db import Base, engine
from data.models.user_model import UserModel
from data.models.organization_model import OrganizationModel
from data.models.department_model import DepartmentModel
from data.models.employee_membership_model import EmployeeMembershipModel
from data.models.department_role_model import DepartmentRoleModel
from data.models.document_model import DocumentModel
from data.models.document_recipient_model import DocumentRecipientModel
from data.models.signature_model import SignatureModel

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Document Signing Service")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(organization_router)
app.include_router(department_router)
app.include_router(employee_router)
app.include_router(access_router)
app.include_router(document_router)
app.include_router(signature_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API is running"}