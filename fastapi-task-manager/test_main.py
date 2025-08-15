# test_main.py

import pytest
from httpx import AsyncClient
from uuid import uuid4
from datetime import datetime

from main import app
from database import get_session
from models import Task, Comment
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "pending",
            "priority": "medium",
            "assignee_id": str(uuid4())
        }
        response = await client.post("/tasks/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == payload["title"]
        assert data["description"] == payload["description"]
        assert data["status"] == payload["status"]
        assert data["priority"] == payload["priority"]

@pytest.mark.asyncio
async def test_get_tasks():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/tasks/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_task():
    # First, create a task
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_payload = {
            "title": "Task to Update",
            "description": "Update me",
            "status": "pending",
            "priority": "low",
            "assignee_id": str(uuid4())
        }
        create_resp = await client.post("/tasks/", json=create_payload)
        task_id = create_resp.json()["id"]

        update_payload = {"status": "in_progress", "priority": "high"}
        update_resp = await client.put(f"/tasks/{task_id}", json=update_payload)
        assert update_resp.status_code == 200
        data = update_resp.json()
        assert data["status"] == "in_progress"
        assert data["priority"] == "high"

@pytest.mark.asyncio
async def test_delete_task():
    # First, create a task
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_payload = {
            "title": "Task to Delete",
            "description": "Delete me",
            "status": "pending",
            "priority": "medium",
            "assignee_id": str(uuid4())
        }
        create_resp = await client.post("/tasks/", json=create_payload)
        task_id = create_resp.json()["id"]

        delete_resp = await client.delete(f"/tasks/{task_id}")
        assert delete_resp.status_code == 204

        # Verify soft delete
        get_resp = await client.get(f"/tasks/{task_id}")
        assert get_resp.status_code == 404

@pytest.mark.asyncio
async def test_create_comment():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a task first
        task_payload = {
            "title": "Task with comment",
            "description": "Task desc",
            "status": "pending",
            "priority": "medium",
            "assignee_id": str(uuid4())
        }
        task_resp = await client.post("/tasks/", json=task_payload)
        task_id = task_resp.json()["id"]

        comment_payload = {
            "content": "This is a test comment",
            "created_by": str(uuid4())
        }
        comment_resp = await client.post(f"/tasks/{task_id}/comments", json=comment_payload)
        assert comment_resp.status_code == 201
        data = comment_resp.json()
        assert data["content"] == comment_payload["content"]
        assert data["task_id"] == task_id

@pytest.mark.asyncio
async def test_get_analytics():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/tasks/analytics")
        assert response.status_code == 200
        data = response.json()
        assert "total_tasks" in data
        assert "status_counts" in data
        assert "priority_counts" in data