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

from sqlalchemy import inspect, text

# 2. Проверяем есть ли колонка role. Если нет — добавляем
with engine.connect() as conn:
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if "users" not in tables:
        print("[ℹ] Таблицы отсутствуют, создаю...")
        Base.metadata.create_all(bind=engine)
    else:
        columns = [c["name"] for c in inspector.get_columns("users")]
        if "role" not in columns:
            print("[ℹ] Колонка 'role' отсутствует, добавляю...")
            conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR NOT NULL DEFAULT 'employee'"))
            conn.commit()
            print("[✓] Колонка 'role' добавлена")
        else:
            print("[✓] Структура таблицы актуальна")

    # Остальные таблицы тоже создаём если нужно
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
        print(f"[ℹ] Admin уже существует: {ADMIN_EMAIL}")
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
