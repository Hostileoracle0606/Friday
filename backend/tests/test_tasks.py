import pytest
from fastapi import status
from datetime import datetime, timedelta


def test_create_task(client, auth_headers):
    """Test creating a task"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z",
        "estimated_time": 60
    }
    
    response = client.post(
        "/api/v1/tasks",
        json=task_data,
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert "id" in data
    assert "user_id" in data


def test_get_tasks(client, auth_headers):
    """Test getting user's tasks"""
    # Create a task first
    task_data = {
        "title": "Test Task",
        "description": "Test description"
    }
    client.post(
        "/api/v1/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    # Get tasks
    response = client.get(
        "/api/v1/tasks",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_task_by_id(client, auth_headers):
    """Test getting a specific task"""
    # Create a task
    task_data = {
        "title": "Test Task",
        "description": "Test description"
    }
    create_response = client.post(
        "/api/v1/tasks",
        json=task_data,
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # Get the task
    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_data["title"]


def test_update_task(client, auth_headers):
    """Test updating a task"""
    # Create a task
    task_data = {
        "title": "Original Title",
        "description": "Original description"
    }
    create_response = client.post(
        "/api/v1/tasks",
        json=task_data,
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # Update the task
    update_data = {
        "title": "Updated Title",
        "status": "in_progress"
    }
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["status"] == update_data["status"]


def test_delete_task(client, auth_headers):
    """Test deleting a task"""
    # Create a task
    task_data = {
        "title": "Task to Delete",
        "description": "This will be deleted"
    }
    create_response = client.post(
        "/api/v1/tasks",
        json=task_data,
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's deleted
    get_response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_create_task_unauthorized(client):
    """Test creating a task without authentication"""
    task_data = {
        "title": "Test Task",
        "description": "Test description"
    }
    response = client.post(
        "/api/v1/tasks",
        json=task_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_tasks_with_filter(client, auth_headers):
    """Test getting tasks with status filter"""
    # Create tasks with different statuses
    task1 = {"title": "Pending Task", "status": "pending"}
    task2 = {"title": "Completed Task", "status": "completed"}
    
    client.post("/api/v1/tasks", json=task1, headers=auth_headers)
    client.post("/api/v1/tasks", json=task2, headers=auth_headers)
    
    # Filter by status
    response = client.get(
        "/api/v1/tasks?status=completed",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(task["status"] == "completed" for task in data)


