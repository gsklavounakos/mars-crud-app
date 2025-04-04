import pytest 
from app import app
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    """Ensures that each test uses the app's client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test for the homepage"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Mars Resource Manager!' in response.data

def test_get_resources(client):
    """Test for getting all resources"""
    response = client.get('/resources')
    assert response.status_code == 200
    assert response.json == []

def test_create_resource(client):
    """Test for creating a new resource"""
    response = client.post('/resources', json={'name': 'Water', 'quantity': 100})
    assert response.status_code == 201
    assert response.json['name'] == 'Water'
    assert response.json['quantity'] == 100

    # Check if resource is actually created
    response = client.get('/resources')
    assert len(response.json) == 1
    assert response.json[0]['name'] == 'Water'

def test_get_resource_by_id(client):
    """Test for getting a specific resource by ID"""
    # Create a resource first
    response = client.post('/resources', json={'name': 'Oxygen', 'quantity': 200})
    resource_id = response.json['id']

    # Get the resource by ID
    response = client.get(f'/resources/{resource_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Oxygen'
    assert response.json['quantity'] == 200

def test_get_resource_by_invalid_id(client):
    """Test for getting a resource that doesn't exist"""
    response = client.get('/resources/999')  # Assuming 999 doesn't exist
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
    response = client.delete('/resources/999')  # Assuming 999 doesn't exist
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'Resource not found'
