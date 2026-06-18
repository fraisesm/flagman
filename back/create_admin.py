"""Скрипт для создания первого admin-аккаунта.
Запускать один раз: python create_admin.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from data.db import SessionLocal
from data.repositories.user_repository import UserRepository
from domain.employee.employee import User
from application.helpers.password_hasher import hash_password

ADMIN_EMAIL = "admin@flagman.ru"
ADMIN_PASSWORD = "admin123"
ADMIN_NAME = "Администратор"
ADMIN_PHONE = "+70000000000"

db = SessionLocal()
repo = UserRepository(db)

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
    print(f"[OK] Admin создан: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")

db.close()
