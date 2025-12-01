import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.config import settings
from app.main import app

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with database override"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "timezone": "UTC"
    }


@pytest.fixture
def auth_headers(client, test_user_data):
    """Register a user and return auth headers"""
    # Register
    response = client.post(
        f"{settings.API_V1_PREFIX}/auth/register",
        json=test_user_data
    )
    assert response.status_code == 201
    
    # Login
    response = client.post(
        f"{settings.API_V1_PREFIX}/auth/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}

