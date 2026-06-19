# Flagman

простите меня, пожалуйста, за этот ужас... 

Сервис документооборота с электронной подписью внутри организации. Руководитель создаёт документы и отправляет их сотрудникам — те читают и подписывают. Все действия фиксируются, статус каждого документа отслеживается в реальном времени.

## Стек

- **Бэкенд** — Python, FastAPI, SQLAlchemy, SQLite (по умолчанию), Alembic
- **Фронтенд** — Vite + Vue
- **Авторизация** — JWT (access token)
- **Подпись** — HMAC по номеру телефона пользователя

## Структура репозитория

```
flagman/
├── back/
│   ├── controllers/        # маршруты FastAPI
│   ├── application/
│   │   ├── commands/       # команды (входные данные хендлеров)
│   │   ├── handlers/       # бизнес-логика
│   │   └── dependencies/   # auth, roles
│   ├── data/
│   │   ├── models/         # ORM-модели
│   │   ├── repositories/   # работа с БД
│   │   └── schemas/        # Pydantic-схемы
│   ├── domain/             # доменные сущности
│   ├── main.py
│   ├── create_admin.py     # скрипт для создания первого admin
│   ├── requirements.txt
│   └── .env.example
└── front/
    ├── src/
    ├── package.json
    └── vite.config.js
```

## Запуск

### Требования

- Python 3.11+
- Node.js 18+

### Бэкенд

```bash
cd back

# создать и активировать виртуальное окружение
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# установить зависимости
pip install -r requirements.txt

# настроить переменные окружения
cp .env.example .env
# открыть .env и заполнить SECRET_KEY (остальное можно оставить как есть)

# запустить
uvicorn main:app --reload --port 8000
```

После запуска Swagger-документация доступна по адресу: http://localhost:8000/docs

### Создание первого администратора

После первого запуска (когда база данных создалась) нужно вручную создать admin-пользователя:

```bash
# находясь в back/ с активированным venv
python create_admin.py
```

### Фронтенд

```bash
cd front
npm install
npm run dev
```

Фронтенд поднимается на http://localhost:5173 и проксирует запросы к бэкенду.

## Переменные окружения

Файл `back/.env.example` содержит все нужные переменные:

| Переменная | Описание | Значение по умолчанию |
|---|---|---|
| `DATABASE_URL` | Строка подключения к БД | `sqlite:///./app.db` |
| `SECRET_KEY` | Секрет для подписи JWT | — (обязательно заполнить) |
| `ALGORITHM` | Алгоритм JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни токена | `60` |

Для PostgreSQL в `DATABASE_URL` нужно указать `postgresql://user:password@host/dbname`.

## Роли

| Роль | Что может |
|---|---|
| `admin` | Всё: управление организацией, пользователями, отделами, назначение ролей |
| `boss` / `manager` / `director` | Создавать и отправлять документы, редактировать и удалять свои |
| `employee` | Просматривать входящие, подписывать документы |

Проверка прав происходит на уровне хендлеров: сначала смотрим `DepartmentRoleModel` (can_send_document), потом — роль в `EmployeeMembership`.

## Жизненный цикл документа

```
[boss создаёт документ]
        ↓
[boss отправляет — одному или всему отделу]
        ↓
   статус: pending          ← документ в inbox у получателя
        ↓
[получатель открывает документ]
        ↓
   статус: read             ← фиксируется автоматически
        ↓
[получатель подписывает]
        ↓
   статус: signed           ← подпись сохраняется в таблице signatures
```

Повторное подписание заблокировано. Статус движется только вперёд: `pending → read → signed`.

## API — основные эндпоинты

### Авторизация

| Метод | Путь | Описание |
|---|---|---|
| POST | `/auth/register` | Регистрация |
| POST | `/auth/login` | Вход, возвращает JWT |
| GET | `/auth/me` | Данные текущего пользователя |

### Документы

| Метод | Путь | Доступ | Описание |
|---|---|---|---|
| POST | `/documents/create` | boss/admin | Создать документ |
| POST | `/documents/send` | boss/admin | Отправить конкретному сотруднику |
| POST | `/documents/send-to-department` | boss/admin | Отправить всему отделу |
| POST | `/documents/forward` | boss/admin | Переслать подписанный документ |
| POST | `/documents/mark-read/{id}` | любой | Отметить как прочитанный |
| GET | `/documents/inbox/{user_id}` | любой | Все входящие |
| GET | `/documents/pending/{user_id}` | любой | Непрочитанные |
| GET | `/documents/unread-count/{user_id}` | любой | Количество непрочитанных |
| POST | `/documents/read-list` | любой | Прочитанные |
| POST | `/documents/signed-list` | любой | Подписанные |
| GET | `/documents/outbox/{user_id}` | любой | Исходящие |
| PUT | `/documents/{id}` | boss/admin | Редактировать (только свой) |
| DELETE | `/documents/{id}` | boss/admin | Удалить (только свой) |

### Подписи

| Метод | Путь | Описание |
|---|---|---|
| POST | `/signatures/sign` | Подписать документ |
| GET | `/signatures/{document_id}` | Посмотреть подписи документа |

### Организация, отделы, сотрудники

| Метод | Путь | Описание |
|---|---|---|
| POST | `/organizations/create` | Создать организацию |
| GET | `/organizations/{id}` | Данные организации |
| POST | `/departments/create` | Создать отдел |
| GET | `/departments/{org_id}` | Отделы организации |
| POST | `/employees/add` | Добавить сотрудника в организацию |
| GET | `/employees/{org_id}` | Список сотрудников |
| POST | `/access/set-role` | Назначить роль в отделе (admin) |

Полный список эндпоинтов с примерами запросов — в Swagger: http://localhost:8000/docs
