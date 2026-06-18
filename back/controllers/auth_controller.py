from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from application.commands.auth.register_user import RegisterUserCommand
from application.commands.auth.login_user import LoginUserCommand
from application.handlers.auth.register_user_handler import RegisterUserHandler
from application.handlers.auth.login_user_handler import LoginUserHandler
from application.dependencies.auth import get_current_user
from data.db import get_db
from data.repositories.user_repository import UserRepository
from data.schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse, UserMeResponse

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
        role=request.role, # type: ignore
    )
    try:
        handler.handle(command)
        return RegisterResponse(message="Пользователь успешно зарегистрирован")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    handler = LoginUserHandler(user_repository)
    command = LoginUserCommand(email=request.email, password=request.password)
    try:
        result = handler.handle(command)
        return LoginResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=UserMeResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserMeResponse)
def update_me(
    request: RegisterRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    from application.helpers.password_hasher import hash_password
    repo = UserRepository(db)
    current_user.full_name = request.full_name
    current_user.email = request.email
    current_user.phone = request.phone
    current_user.password = hash_password(request.password)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/users", response_model=list[UserMeResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Только для admin — полный список пользователей"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    return UserRepository(db).get_all()


@router.get("/users-public", response_model=list[UserMeResponse])
def get_users_public(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Доступно всем авторизованным пользователям — для выбора получателя.
    Возвращает только базовые поля: id, full_name, email, role."""
    return UserRepository(db).get_all()
