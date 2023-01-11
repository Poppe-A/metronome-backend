import pytest
from app import create_app
from app.db_init import db

@pytest.fixture()
def app():
    app = create_app(test=True)
    yield app
    
@pytest.fixture()
def client(app):
    yield app.test_client()