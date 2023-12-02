import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

class DevelopmentConfig:
    DEBUG = True
    DATABASE_NAME = os.getenv('DATABASE_NAME') | 'autogro'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite')
    SECRET_KEY = 'secret-key-goes-here'

class TestingConfig(DevelopmentConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    
class ProductionConfig(DevelopmentConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')