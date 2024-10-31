from app import app, bcrypt, fetch_weather_data, fetch_forecast
import pytest
from models import db

@pytest.fixture(scope='module')
def test_client():
    app.config.from_object('config.TestingConfig')
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_password_hashing():
    """Test that passwords are hashed and validated correctly."""
    password = 'mypassword'
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    assert bcrypt.check_password_hash(hashed_pw, password)  

def test_fetch_weather_data():
    """Test that weather data is correctly retrieved for a valid city."""
    weather_data = fetch_weather_data("Houston")
    assert weather_data is not None
    assert 'temp' in weather_data
    assert 'conditions' in weather_data
    assert 'icon' in weather_data

def test_fetch_forecast():
    """Test that forecast data is correctly retrieved for a valid city."""
    forecast_data = fetch_forecast("Houston")
    assert forecast_data is not None
    assert isinstance(forecast_data, dict)  


