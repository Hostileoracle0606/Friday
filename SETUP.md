# Friday - Setup Guide

## Quick Start

### Option 1: Docker Compose (Recommended)

1. Navigate to the `infra` directory:
```bash
cd infra
```

2. Copy environment file (if needed):
```bash
cp .env.example .env
# Edit .env with your SECRET_KEY
```

3. Start all services:
```bash
docker-compose up -d
```

4. Run database migrations:
```bash
docker-compose exec backend alembic upgrade head
```

5. Access the API:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Prerequisites
- Python 3.11+
- PostgreSQL 14+

#### Backend Setup

1. Create and activate virtual environment:
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Copy the template
cp env_template.txt .env
# Edit .env with your database credentials and secret key
```

4. Create PostgreSQL database:
```sql
CREATE DATABASE friday_db;
```

5. Run migrations:
```bash
alembic upgrade head
```

6. Start the server:
```bash
uvicorn app.main:app --reload
```

## Testing the API

### 1. Register a User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "timezone": "UTC"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

Save the `access_token` from the response.

### 3. Create a Task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Complete project",
    "description": "Finish the Friday app",
    "due_date": "2024-12-31T23:59:59Z",
    "estimated_time": 120
  }'
```

### 4. Create a Journal Entry
```bash
curl -X POST "http://localhost:8000/api/v1/journal" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "content": "Today was a productive day. I finished the backend setup."
  }'
```

## Project Structure

```
Friday/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── core/        # Core configuration and utilities
│   │   ├── models/      # SQLAlchemy models
│   │   ├── routes/      # API route handlers
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   ├── alembic/         # Database migrations
│   └── requirements.txt
├── frontend/            # React frontend (to be implemented)
├── services/            # Microservices (to be implemented)
└── infra/               # Docker and deployment configs
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user profile

### Tasks
- `GET /api/v1/tasks` - List user's tasks (query params: skip, limit, status)
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks/{id}` - Get task by ID
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

### Journal
- `POST /api/v1/journal` - Submit journal entry
- `GET /api/v1/journal` - Get journal history (query params: skip, limit, since)
- `GET /api/v1/journal/{id}` - Get specific entry

## Database Migrations

Create a new migration:
```bash
cd backend
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback:
```bash
alembic downgrade -1
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check `DATABASE_URL` in `.env` file
- Verify database exists: `CREATE DATABASE friday_db;`

### Migration Issues
- Make sure all models are imported in `alembic/env.py`
- Check that `DATABASE_URL` is set correctly

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

