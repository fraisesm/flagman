class GetDepartmentQuery:
    def __init__(self, department_id: int):
        self.department_id = department_id


class ListDepartmentsQuery:
    def __init__(self, organization_id: int):
        self.organization_id = organization_id
