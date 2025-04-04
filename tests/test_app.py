import pytest
from app import app as flask_app
from app import get_db

@pytest.fixture
def app():
    # Configure the app for testing and set up an in-memory database
    flask_app.config['TESTING'] = True
    flask_app.config['DATABASE'] = ':memory:'  # Use in-memory database

    # Create the resources table
    with flask_app.app_context():
        db = get_db()
        db.execute('CREATE TABLE resources (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, quantity INTEGER NOT NULL)')
        yield flask_app

@pytest.fixture
def client(app):
    # Create the client for tests
    return app.test_client()

# Tests for the endpoints
def test_get_resources(client):
    """Test for retrieving all resources"""
    response = client.get('/resources')
    assert response.status_code == 200
    assert response.json == []

def test_create_resource(client):
    """Test for creating a new resource"""
    response = client.post('/resources', json={'name': 'Water', 'quantity': 100})
    assert response.status_code == 201
    assert response.json['name'] == 'Water'
    assert response.json['quantity'] == 100

    response = client.get('/resources')
    assert len(response.json) == 1
    assert response.json[0]['name'] == 'Water'

def test_get_resource_by_id(client):
    """Test for retrieving a specific resource by ID"""
    # Create a resource first
    response = client.post('/resources', json={'name': 'Oxygen', 'quantity': 200})
    resource_id = response.json['id']

    # Get the resource by ID
    response = client.get(f'/resources/{resource_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Oxygen'
    assert response.json['quantity'] == 200

def test_get_resource_by_invalid_id(client):
    """Test for retrieving a resource that doesn't exist"""
    response = client.get('/resources/999')  # Assuming ID 999 doesn't exist
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'Resource not found'

def test_update_resource(client):
    """Test for updating a resource"""
    # Create a resource first
    response = client.post('/resources', json={'name': 'Water', 'quantity': 100})
    resource_id = response.json['id']

    # Update the resource
    response = client.put(f'/resources/{resource_id}', json={'name': 'Water', 'quantity': 150})
    assert response.status_code == 200
    assert response.json['name'] == 'Water'
    assert response.json['quantity'] == 150

def test_update_resource_not_found(client):
    """Test for updating a resource that doesn't exist"""
    response = client.put('/resources/999', json={'name': 'Water', 'quantity': 150})
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'Resource not found'

def test_delete_resource(client):
    """Test for deleting a resource"""
    # Create a resource first
    response = client.post('/resources', json={'name': 'Water', 'quantity': 100})
    resource_id = response.json['id']

    # Delete the resource
    response = client.delete(f'/resources/{resource_id}')
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['message'] == 'Resource deleted successfully'

    # Verify it's deleted
    response = client.get(f'/resources/{resource_id}')
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'Resource not found'

def test_delete_resource_not_found(client):
    """Test for deleting a resource that doesn't exist"""
    response = client.delete('/resources/999')  # Assuming ID 999 doesn't exist
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'Resource not found'
