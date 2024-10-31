# tests/test_routes.py

import pytest
from app import app, db
from models import User

@pytest.fixture(scope='module')
def test_client():
    app.config.from_object('config.TestingConfig')
    
    with app.app_context():
        db.create_all()
        client = app.test_client()
        yield client
        db.drop_all()

@pytest.fixture(scope='function', autouse=True)
def session_scope():
    db.session.begin_nested()
    yield
    db.session.rollback()

def test_register_user(test_client):
    """Test user registration."""
    response = test_client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Account created successfully. Welcome testuser!" in response.data

def login(test_client, email, password):
    """Helper function to log in a user."""
    return test_client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def test_login_user(test_client):
    """Test user login."""
    
    test_client.post('/register', data={
        'username': 'testuser2',
        'email': 'testuser2@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    
    login_response = login(test_client, 'testuser2@example.com', 'password123')
    assert login_response.status_code == 200
    assert b"Login successful! Welcome back, testuser2!" in login_response.data

def test_add_favorite_city(test_client):
    """Test adding a city to favorites."""
   
    login_response = login(test_client, 'testuser2@example.com', 'password123')
    assert login_response.status_code == 200

    response = test_client.post('/add_favorite', data={
        'city_name': 'Miami'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Miami added to favorites!" in response.data

def test_get_weather_info(test_client):
    """Test retrieving weather info for a specific city."""
    
    login_response = login(test_client, 'testuser2@example.com', 'password123')
    assert login_response.status_code == 200
    assert b"Login successful! Welcome back, testuser2!" in login_response.data

    response = test_client.get('/weather?location=Houston', follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Houston" in response.data  
    assert b"Temperature:" in response.data  
    assert b"Condition:" in response.data 

