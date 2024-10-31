import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'  

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql:///quikweather_test_db'
    TESTING = True
    DEBUG = True
