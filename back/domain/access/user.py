class User:
    def __init__(self, full_name: str, email: str, phone: str, hashed_password: str):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.hashed_password = hashed_password