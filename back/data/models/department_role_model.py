from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from data.db import Base


class DepartmentRoleModel(Base):
    __tablename__ = "department_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    role_name = Column(String, nullable=False)

    can_send_document = Column(Boolean, default=False)
    can_sign_document = Column(Boolean, default=False)
    can_manage_department = Column(Boolean, default=False)