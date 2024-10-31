import pytest
from models import User, City, Favorite, db
from app import app

@pytest.fixture(scope='module')
def test_client():
    app.config.from_object('config.TestingConfig')
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_unique_favorite_constraint(test_client):
    """Test that a user cannot add the same city as a favorite more than once."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com', password_hash='hashed_pw')
        city = City(name='New York', country='US', latitude=40.7128, longitude=-74.0060)
        db.session.add_all([user, city])
        db.session.commit()
        
        favorite1 = Favorite(user_id=user.id, city_id=city.id)
        favorite2 = Favorite(user_id=user.id, city_id=city.id)
        
        db.session.add(favorite1)
        db.session.commit()
        
        with pytest.raises(Exception):  # Adding the duplicate should raise an exception
            db.session.add(favorite2)
            db.session.commit()

def test_city_coordinate_constraints(test_client):
    """Test that city latitude and longitude constraints are enforced."""
    with app.app_context():
        # Valid latitude and longitude
        valid_city = City(name='ValidCity', country='US', latitude=45.0, longitude=-75.0)
        db.session.add(valid_city)
        db.session.commit()
        
        # Invalid latitude
        with pytest.raises(Exception):
            invalid_city = City(name='InvalidCity', country='US', latitude=100.0, longitude=-75.0)
            db.session.add(invalid_city)
            db.session.commit()
