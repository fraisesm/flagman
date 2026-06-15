class RegisterUserCommand:
    def __init__(self, full_name: str, email: str, phone: str, password: str):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.password = password