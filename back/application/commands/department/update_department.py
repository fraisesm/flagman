class UpdateDepartmentCommand:
    def __init__(self, department_id: int, name: str, description: str = None):
        self.department_id = department_id
        self.name = name
        self.description = description
