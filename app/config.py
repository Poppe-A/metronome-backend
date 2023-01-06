import os

class Config(object) :
    FLASK_HOST = os.getenv('HOST', '0.0.0.0')
    FLASK_PORT = os.getenv('PORT', 5000)
    FLASK_DEBUG = os.getenv('DEBUG', True)
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost:2345')
    DB_NAME = os.getenv('DB_NAME', 'logme')