import os

class Config(object) :
    FLASK_HOST = os.getenv('HOST', '0.0.0.0')
    FLASK_PORT = os.getenv('PORT', 5000)
    FLASK_DEBUG = os.getenv('DEBUG', True)
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
    DB_NAME = os.getenv('DB_NAME', 'logme')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SECRET_KEY = 'super secret string'
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{os.getenv("DB_USER", "postgres")}:{os.getenv("DB_PASSWORD", "postgres")}@{os.getenv("DB_HOST", "localhost:5432")}/{os.getenv("DB_NAME", "logme")}'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/logme'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@db/postgres'

class TestConfig(Config):
    TESTING = True
    LOGIN_DISABLED = True
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{os.getenv("DB_USER", "postgres")}:{os.getenv("DB_PASSWORD", "postgres")}@{os.getenv("DB_HOST", "localhost:5432")}/test_logme'

class DevConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False


