import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql:///quik_weather')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql:///quikweather_test_db'
    TESTING = True
    DEBUG = True
