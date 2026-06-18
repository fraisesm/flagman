class User:
    def __init__(self, full_name: str, email: str, phone: str, password: str, role: str = "employee"):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.password = password
        self.role = role
