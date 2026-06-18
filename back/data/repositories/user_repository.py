from sqlalchemy.orm import Session

from data.models.user_model import UserModel
from domain.employee.employee import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def get_by_id(self, user_id: int):
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_all(self):
        return self.db.query(UserModel).all()

    def create(self, user: User):
        user_model = UserModel(
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            password=user.password,
            role=user.role,
        )
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)
        return user_model
