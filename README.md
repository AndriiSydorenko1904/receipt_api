## Receipt API

### Description
A REST API service for creating and viewing purchase receipts, featuring:
- JWT авторизації
- CRUD для чеків
- Публічного перегляду чеку
- Фільтрації, пагінації
- Опціональних pytest тестів

### Technologies
- Python 3.11+
- FastAPI
- PostgreSQL
- Alembic
- JWT (PyJWT)
- Pydantic
- Uvicorn

### Project Structure
```
receipt_api/
├── app/
│   ├── __init__.py
│   ├── main.py                    ← entry point (uvicorn app.main:app)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings.py           ← config (SECRET_KEY, DB, tokens)
│   │   ├── database.py           ← async engine + get_db
│   │   └── security.py           ← JWT/token logic, password hashing
│
│   ├── models/
│   │   ├── __init__.py           ← import all models
│   │   ├── user.py
│   │   └── receipt.py
│
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── receipt.py
│
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py              ← /users/register, /users/login
│   │   ├── receipts.py           ← authenticated user receipts
│   │   └── public.py             ← public receipt in text format
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_receipts.py
│   └── test_public.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── requirements.txt
├── docker-compose.yml           ← for PostgreSQL
├── alembic.ini
├── Makefile                     ← command shortcuts
└── README.md                    ← project description, API, setup
```

### Встановлення

```bash
make create_env  # create a virtual environment
make install     # install dependencies
make up          # run postgres in docker
make migrate     # apply migrations
make runserver   # run locally on :8000
```

### Database Structure
- User(id, name, login, hashed_password)
- Receipt(id, created_at, total, user_id, payment_type, payment_amount, rest)
- ReceiptProduct(id, receipt_id, name, price, quantity, total_price)

### API (Swagger available)
- POST /users/register
- POST /users/login
- POST /receipts
- GET /receipts
- GET /receipts/{id}
- GET /receipts/public/{id}?line_length=32

### Testing
```bash
make test
```
