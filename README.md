## Receipt API

### Description
A REST API service for creating and viewing purchase receipts, featuring:
- JWT authorization
- CRUD for receipts
- Public receipt viewing
- Filtering, pagination
- Optional test cases

### ✅ Requirements

- Python 3.11+
- Poetry or pip + virtualenv
- Docker (for PostgreSQL via docker-compose)
- Make (optional but recommended)

### Project Structure
```
receipt_api/
├── app/
│   ├── __init__.py
│   ├── main.py                   ← entry point (uvicorn app.main:app)
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

### Installation and run

```bash
make create_env  # create a virtual environment
make install     # install dependencies
make up          # start postgres via docker
make migrate     # apply migrations
make runserver   # run locally on :8000
```

### Database Structure

- User(id, name, login, hashed_password)
- Receipt(id, created_at, total, user_id, payment_type, payment_amount, rest)
- ReceiptProduct(id, receipt_id, name, price, quantity, total_price)

### 📬 API Endpoints (Swagger)

Method | Endpoint                 | Description
-------|--------------------------|------------------------------
POST   | /users/register          | Register a new user
POST   | /users/login             | Log in and obtain JWT
POST   | /receipts                | Create a new receipt
GET    | /receipts                | Get user receipts (with filters)
GET    | /receipts/{id}           | Get specific user receipt
GET    | /receipts/public/{id}    | Public, text-mode receipt preview

### Testing
```bash
make test
```

### 💡 Notes

- Environment variables can be configured in app/core/settings.py
- PostgreSQL runs on localhost:5432 as per docker-compose.yml
- You can tweak line formatting for public receipts via ?line_length=N
