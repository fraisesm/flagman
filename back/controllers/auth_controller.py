from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from application.commands.auth.register_user import RegisterUserCommand
from application.handlers.auth.register_user_handler import RegisterUserHandler
from data.db import get_db
from data.repositories.user_repository import UserRepository
from data.schemas.auth import RegisterRequest, RegisterResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    handler = RegisterUserHandler(user_repository)

    command = RegisterUserCommand(
        full_name=request.full_name,
        email=request.email,
        phone=request.phone,
        password=request.password,
    )

    try:
        handler.handle(command)
        return RegisterResponse(message="Пользователь успешно зарегистрирован")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))