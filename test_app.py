# Import necessary modules for testing
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from app import create_app, db, Task
import pytest
from app import create_app, db, Task
print("Running test_app.py")

@pytest.fixture
def client():
    """
    Pytest fixture to set up a test client with an in-memory SQLite database.
    """
    app = create_app()
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Use in-memory database for testing
        'TESTING': True,  # Enable testing mode
    })

    with app.app_context():
        db.create_all()  # Create tables

        with app.test_client() as client:
            yield client  # Provide the test client to the test functions

        db.session.remove()  # Clean up the session
        db.drop_all()  # Drop all tables

def test_create_task(client):
    """
    Test the creation of a new task.
    """
    assert Task.query.count() == 0  # Ensure no tasks exist initially
    response = client.post('/tasks', json={'title': 'New Task'})
    assert response.status_code == 200
    assert b'New Task' in response.data
    assert Task.query.count() == 1  # Ensure one task was added

def test_delete_task(client):
    """
    Test the deletion of a task.
    """
    client.post('/tasks', json={'title': 'To be deleted'})
    assert Task.query.count() == 1
    response = client.delete('/tasks/title/To be deleted')
    assert response.status_code == 204
    assert Task.query.count() == 0  # Ensure the task was deleted

def test_mark_task_complete(client):
    """
    Test marking a task as completed.
    """
    client.post('/tasks', json={'title': 'Task to complete'})
    task = Task.query.first()
    response = client.patch(f'/tasks/{task.id}/complete')
    assert response.status_code == 200
    assert Task.query.get(task.id).completed == True  # Ensure the task is marked as completed

def test_update_task(client):
    """
    Test updating the title of a task.
    """
    client.post('/tasks', json={'title': 'title1'})
    task = Task.query.first()
    response = client.put(f'/tasks/{task.id}', json={'title': 'title2'})
    assert response.status_code == 200
    updated_task = Task.query.get(task.id)
    assert updated_task.title == 'title2'  # Ensure the title was updated

def test_get_task(client):
    """
    Test retrieving a single task by ID.
    """
    client.post('/tasks', json={'title': 'Sample Task'})
    task = Task.query.first()
    response = client.get(f'/tasks/{task.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Sample Task'  # Ensure the correct task is retrieved

print("Loaded test_app.py")
print("real_test.py is being executed")
