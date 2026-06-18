from application.commands.auth.login_user import LoginUserCommand
from application.helpers.jwt_helper import create_access_token
from application.helpers.password_hasher import verify_password
from data.repositories.user_repository import UserRepository


class LoginUserHandler:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def handle(self, command: LoginUserCommand) -> str:
        user = self.user_repository.get_by_email(command.email)
        if not user or not verify_password(command.password, user.password):
            raise ValueError("Неверный email или пароль")
        return create_access_token({"sub": str(user.id)})
