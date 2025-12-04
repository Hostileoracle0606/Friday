# Friday - Personal Assistant App

A mood-aware personal assistant application that helps manage tasks, journaling, and scheduling based on emotional state and productivity patterns.

## Features

- **User Authentication**: Secure JWT-based authentication
- **Task Management**: Full CRUD operations for tasks with priority tracking
- **Journaling**: Submit and track journal entries with mood analysis
- **Mood Integration**: (Coming in Phase 3) Text and behavioral mood analysis
- **Priority Engine**: (Coming in Phase 4) Extended Eisenhower matrix with mood augmentation
- **Calendar Integration**: (Coming in Phase 2) Brightspace and Google Calendar sync

## Project Structure

```
Friday/
├── backend/          # FastAPI backend application
├── frontend/         # React frontend (to be implemented)
├── services/         # Microservices (mood, ingestion)
└── infra/            # Docker, deployment configurations
```

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Docker and Docker Compose (optional)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Docker Setup

1. Start all services:
```bash
docker-compose -f infra/docker-compose.yml up -d
```

2. Run migrations:
```bash
docker-compose -f infra/docker-compose.yml exec backend alembic upgrade head
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user profile

### Tasks
- `GET /tasks` - List user's tasks
- `POST /tasks` - Create new task
- `GET /tasks/{id}` - Get task by ID
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

### Journal
- `POST /journal` - Submit journal entry
- `GET /journal` - Get journal history
- `GET /journal/{id}` - Get specific entry

## Development

### Running Tests
```bash
pytest
```

### Code Quality
```bash
# Linting
ruff check backend/

# Type checking
mypy backend/
```

## License

MIT


