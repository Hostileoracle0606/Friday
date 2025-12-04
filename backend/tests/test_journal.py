import pytest
from fastapi import status
from datetime import datetime, timedelta


def test_create_journal_entry(client, auth_headers):
    """Test creating a journal entry"""
    entry_data = {
        "content": "Today was a great day! I finished the backend setup.",
        "mood_label": "happy"
    }
    
    response = client.post(
        "/api/v1/journal",
        json=entry_data,
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["content"] == entry_data["content"]
    assert data["mood_label"] == entry_data["mood_label"]
    assert "id" in data
    assert "user_id" in data
    assert "created_at" in data


def test_get_journal_entries(client, auth_headers):
    """Test getting journal entries"""
    # Create an entry first
    entry_data = {
        "content": "Test journal entry"
    }
    client.post(
        "/api/v1/journal",
        json=entry_data,
        headers=auth_headers
    )
    
    # Get entries
    response = client.get(
        "/api/v1/journal",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_journal_entry_by_id(client, auth_headers):
    """Test getting a specific journal entry"""
    # Create an entry
    entry_data = {
        "content": "Specific entry"
    }
    create_response = client.post(
        "/api/v1/journal",
        json=entry_data,
        headers=auth_headers
    )
    entry_id = create_response.json()["id"]
    
    # Get the entry
    response = client.get(
        f"/api/v1/journal/{entry_id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == entry_id
    assert data["content"] == entry_data["content"]


def test_get_journal_entries_with_date_filter(client, auth_headers):
    """Test getting journal entries with date filter"""
    # Create entries
    entry1 = {"content": "Old entry"}
    entry2 = {"content": "Recent entry"}
    
    client.post("/api/v1/journal", json=entry1, headers=auth_headers)
    client.post("/api/v1/journal", json=entry2, headers=auth_headers)
    
    # Filter by date (last 24 hours)
    since = (datetime.utcnow() - timedelta(hours=24)).isoformat() + "Z"
    response = client.get(
        f"/api/v1/journal?since={since}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)


def test_create_journal_entry_unauthorized(client):
    """Test creating a journal entry without authentication"""
    entry_data = {
        "content": "Test entry"
    }
    response = client.post(
        "/api/v1/journal",
        json=entry_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_journal_entries_ordered_by_date(client, auth_headers):
    """Test that journal entries are ordered by date (newest first)"""
    # Create multiple entries
    for i in range(3):
        entry_data = {"content": f"Entry {i}"}
        client.post("/api/v1/journal", json=entry_data, headers=auth_headers)
    
    # Get entries
    response = client.get("/api/v1/journal", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Check ordering (newest first)
    if len(data) > 1:
        dates = [datetime.fromisoformat(entry["created_at"].replace("Z", "+00:00")) for entry in data]
        assert dates == sorted(dates, reverse=True)


