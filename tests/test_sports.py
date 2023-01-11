import json

def test_add_sport(client):
    print('-----------------------------------------')
    data = {
        'name': "sport3",
    }
    response = client.post('/sports/add', data=json.dumps(data))
    print("[test_add_sport] response", response.data)
    assert len(response.data) > 1

def test_get_sports(client):
    print('-----------------------------------------')
    response = client.get('/sports/all')
    print("[test_sports] response", response.json)
    assert len(response.json) > 1

