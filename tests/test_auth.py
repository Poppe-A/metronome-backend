import json
from flask_login import current_user

def test_login_required_user_not_logged(client):
    print('-----------------------------------------')

    print("[test_login_required_not_logged] - Should not access this route if not logged")
    response = client.post('/auth/account1')
    assert response.status_code == 405

def test_signup(client):
    print('-----------------------------------------')

    data = {
        "name": "testUser",
        "email": "test@user.com",
        "password": "test"
    }
    response = client.post('/auth/signup', data=json.dumps(data))
    print("[test_signup] - ", "Should be able to create a new user or indicate if user", response.json['status'])

    assert response.json['status']

def test_login(client):
    print('-----------------------------------------')

    data = {
        "email": "test@user.com",
        "password": "tefst"
    }

    response = client.post('/auth/login', data=json.dumps(data))
    print("[test_login] - ", "Should be able to log with previously created user", response.data)
    assert response.json['status'] == 200

def test_login_current_user(client):
    data = {
        "email": "test@user.com",
        "password": "test"
    }

    with client:
        client.post('/auth/login', data=json.dumps(data))
        # success
        response = client.get('/auth/test')
        print('[test_login_required_user_logged] - Should access protected route since user is logged')
        print(response)
        assert current_user.id == 1

