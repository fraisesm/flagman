# Flagman — Document Signing Service

## Структура

```
flagman/
├── back/       # FastAPI бэкенд
└── front/      # Vite фронтенд
```

## Быстрый старт

### Бэкенд

```bash
cd back
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # заполнить .env
uvicorn main:app --reload --port 8000
```

Документация API: http://localhost:8000/docs

### Фронтенд

```bash
cd front
npm install
npm run dev
```

## Роли

| Роль | Права |
|---|---|
| `admin` | Всё |
| `boss` | Создание и отправка документов |
| `employee` | Просмотр и подписание документов |

## Жизненный цикл документа

```
Создание → Отправка → Прочтение → Подписание
pending        →  read      →  signed
```
