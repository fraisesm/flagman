from sqlalchemy import Column, ForeignKey, Integer, String

from data.db import Base


class EmployeeMembershipModel(Base):
    __tablename__ = "employee_memberships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    role = Column(String, nullable=True)