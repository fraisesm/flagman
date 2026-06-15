from application.commands.auth.register_user import RegisterUserCommand
from data.repositories.user_repository import UserRepository
from domain.employee.employee import User


class RegisterUserHandler:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def handle(self, command: RegisterUserCommand):
        existing_user = self.user_repository.get_by_email(command.email)
        if existing_user:
            raise ValueError("Пользователь с таким email уже существует")

        user = User(
            full_name=command.full_name,
            email=command.email,
            phone=command.phone,
            password=command.password,
        )

        return self.user_repository.create(user)