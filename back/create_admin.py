"""Скрипт для создания первого admin-аккаунта.
Запускать один раз: python create_admin.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# 1. Импортируем ВСЕ модели чтобы SQLAlchemy их зарегистрировал
from data.db import Base, engine, SessionLocal
import data.models.user_model  # noqa
import data.models.organization_model  # noqa
import data.models.department_model  # noqa
import data.models.employee_membership_model  # noqa
import data.models.department_role_model  # noqa
import data.models.document_model  # noqa
import data.models.document_recipient_model  # noqa
import data.models.signature_model  # noqa

# 2. Создаём таблицы (если уже есть — ничего не случится)
Base.metadata.create_all(bind=engine)
print("[✓] Таблицы готовы")

from data.repositories.user_repository import UserRepository
from domain.employee.employee import User
from application.helpers.password_hasher import hash_password

ADMIN_EMAIL = "admin@flagman.ru"
ADMIN_PASSWORD = "admin123"
ADMIN_NAME = "Администратор"
ADMIN_PHONE = "+70000000000"

db = SessionLocal()
repo = UserRepository(db)

try:
    existing = repo.get_by_email(ADMIN_EMAIL)
    if existing:
        print(f"[INFO] Admin уже существует: {ADMIN_EMAIL}")
    else:
        admin = User(
            full_name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            phone=ADMIN_PHONE,
            password=hash_password(ADMIN_PASSWORD),
            role="admin",
        )
        repo.create(admin)
        print("[OK] Admin успешно создан!")
        print(f"     Email:  {ADMIN_EMAIL}")
        print(f"     Пароль: {ADMIN_PASSWORD}")
finally:
    db.close()
