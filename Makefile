# Start PostgreSQL with Docker
up:
	docker compose up -d

# Stop Docker containers
down:
	docker compose down

# Install Python dependencies
install:
	. .env/bin/activate && pip install -r requirements.txt

# Create an environment
create_env:
	python3 -m venv .env

# Create a new Alembic migration and apply it
migrate:
	. .env/bin/activate && alembic revision --autogenerate -m "migration"
	. .env/bin/activate && alembic upgrade head

# Apply all Alembic migrations
upgrade:
	. .env/bin/activate && alembic upgrade head

# Run FastAPI development server
runserver:
	. .env/bin/activate && uvicorn app.main:app --reload

# Run tests with pytest and suppress asyncio warnings
test:
	. .env/bin/activate && PYTHONPATH=. pytest -v

# Clean Python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +

