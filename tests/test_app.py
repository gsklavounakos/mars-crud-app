import pytest
from app import app

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
