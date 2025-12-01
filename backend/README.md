# Friday Backend

FastAPI backend for the Friday personal assistant application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT tokens
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `DEBUG`: Debug mode (default: False)
- `API_V1_PREFIX`: API prefix (default: /api/v1)

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

