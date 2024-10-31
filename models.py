from sqlalchemy import func, CheckConstraint
from sqlalchemy.orm import validates
from extensions import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_login = db.Column(db.Boolean, default=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50))
    latitude = db.Column(db.Float, CheckConstraint('latitude >= -90 and latitude <= 90'))
    longitude = db.Column(db.Float, CheckConstraint('longitude >= -180 and longitude <= 180'))
    weather = db.relationship('Weather', uselist=False, backref='city')
    favorites = db.relationship('Favorite', backref='city', lazy=True)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    __table_args__ = (db.UniqueConstraint('user_id', 'city_id', name='user_city_uc'),)
   
class Weather(db.Model):
    __tablename__ = 'weather'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False, unique=True)
    current_temp = db.Column(db.Float)
    current_conditions = db.Column(db.String(50))
    high_temp = db.Column(db.Float)
    forecast = db.Column(db.JSON)
    last_updated = db.Column(db.DateTime, server_default=func.now())

