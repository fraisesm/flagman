from application.queries.department.get_department_query import GetDepartmentQuery, ListDepartmentsQuery
from data.repositories.department_repository import DepartmentRepository


class GetDepartmentHandler:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository

    def handle(self, query: GetDepartmentQuery):
        dept = self.repository.get_by_id(query.department_id)
        if not dept:
            raise ValueError("Отдел не найден")
        return dept


class ListDepartmentsHandler:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository

    def handle(self, query: ListDepartmentsQuery):
        return self.repository.get_all_by_organization(query.organization_id)
