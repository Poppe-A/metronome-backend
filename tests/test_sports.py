import json
from flask_jwt_extended import create_access_token

def getHeaders():
    return {'Authorization': f'Bearer {jwt}'}

def log_user(client):
    data = {
        "email": "test@user.com",
        "password": "test"
    }

    result = client.post('/auth/login', data=json.dumps(data))
    print('------ result', result.json["jwt"])
    headers = {
        'Authorization': f'Bearer {result.json["jwt"]}'
    }
    jwt = result.json["jwt"]
    response = client.get('/auth/currentUser', headers=headers)
    print('[test_login_required_user_logged] - Should access protected route since user is logged')
    print(response.json["logged_in_as"])
    assert response.json["logged_in_as"]["email"] == "test@user.com"


def test_add_sport(client):
    print('-----------------------------------------')
    data = {
        'name': "Sport test",
    }
    response = client.post('/sports/add', data=json.dumps(data))
    print("[test_add_sport] response", response.data)
    assert len(response.data) > 1


def test_get_sports(client):
    print('-----------------------------------------')
    response = client.get('/sports/all')
    print("[test_sports] response", response.json)
    assert response.json[0]["id"] == 1


def test_associate_sport(client):
    print('-----------------------------------------')
    data = {
        "name": "session 1", 
        "sport_id": 1,
        "user_id": 1
    }

    with client.application.app_context():
        access_token = create_access_token({'id': 1})
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = client.post('/sports/associateSport', headers=headers, data=json.dumps(data))
        print("[test_associate_sport] response", response.data)
        assert response.data.decode('UTF-8') == 'Sport test associated to user 1'


def test_create_session(client):
    print('-----------------------------------------')
    data = {
        "session_name": "session 1", 
        "sport_id": 1
    }

    with client.application.app_context():
        access_token = create_access_token({'id': 1})
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = client.post('/sports/createSession', data=json.dumps(data), headers=headers)
        print("[test_create_session] response", response.json)
        assert response.data.decode('UTF-8') == "session added"


def test_get_sessions(client):
    print('-----------------------------------------')

    with client.application.app_context():
        access_token = create_access_token({'id': 1})
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = client.get('/sports/sessions', headers=headers)
        print("[test_get_session] response", response.json)
        assert response.json[0]["name"] == "session 1"


def test_get_session_with_id(client):
    print('-----------------------------------------')
    with client.application.app_context():
        access_token = create_access_token({'id': 1})
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
    response = client.get('/sports/sessions/1', headers=headers)
    print("[test_get_session_with_id] response", response.json, headers)
    assert response.json["name"] == "session 1"
