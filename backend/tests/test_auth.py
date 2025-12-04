import pytest
from fastapi import status


def test_register_user(client, test_user_data):
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json=test_user_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client, test_user_data):
    """Test that duplicate email registration fails"""
    # First registration
    response = client.post(
        "/api/v1/auth/register",
        json=test_user_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    
    # Duplicate registration
    response = client.post(
        "/api/v1/auth/register",
        json=test_user_data
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_success(client, test_user_data):
    """Test successful login"""
    # Register first
    client.post(
        "/api/v1/auth/register",
        json=test_user_data
    )
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, test_user_data):
    """Test login with invalid credentials"""
    # Register first
    client.post(
        "/api/v1/auth/register",
        json=test_user_data
    )
    
    # Login with wrong password
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user_data["email"],
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client, auth_headers):
    """Test getting current user profile"""
    response = client.get(
        "/api/v1/auth/me",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "email" in data
    assert "id" in data


def test_get_current_user_unauthorized(client):
    """Test getting current user without authentication"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


