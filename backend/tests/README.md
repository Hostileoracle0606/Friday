# Testing

## Setup

Tests require all backend dependencies to be installed. For best results, use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Note: On Windows, you may need to install PostgreSQL development libraries for psycopg2-binary, or use Docker for testing.

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_register_user
```

## Test Coverage

Tests cover:
- User authentication (register, login, current user)
- Task CRUD operations
- Journal entry operations
- Authorization checks
- Data validation

## Test Database

Tests use SQLite in-memory database for speed and isolation. Each test gets a fresh database.


