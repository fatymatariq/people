import base64
from people_api.constants import TOKEN_ENDPOINT, USERS_ENDPOINT


def test_users_post(client):
    new_user = {"username": "test1", "password": "FlaskIsAwesome"}
    response = client.post(USERS_ENDPOINT, json=new_user)
    assert response.status_code == 201
    assert response.json["id"]
    assert response.json["username"] == "test1"
    
def test_users_post_duplicate(client):
    new_user = {"username": "test1", "password": "FlaskIsAwesome"}
    response = client.post(USERS_ENDPOINT, json=new_user)
    assert response.status_code == 406

def test_users_post_missing_username(client):
    new_user = {"password": "FlaskIsAwesome"}
    response = client.post(USERS_ENDPOINT, json=new_user)
    assert response.status_code == 400

def test_users_post_missing_password(client):
    new_user = {"username": "test1"}
    response = client.post(USERS_ENDPOINT, json=new_user)
    assert response.status_code == 400

def test_get_single_user(client, token_header):
    response = client.get(f"{USERS_ENDPOINT}/2", headers=token_header)
    assert response.status_code == 200
    assert response.json["username"] == "test1"

def test_get_single_user_not_found(client, token_header):
    response = client.get(f"{USERS_ENDPOINT}/3", headers=token_header)
    assert response.status_code == 404

def test_get_single_user_invalid_token(client):
    headers = {"Authorization": f"Bearer 1234567890"}
    response = client.get(f"{USERS_ENDPOINT}/2", headers=headers)
    assert response.status_code == 401

def test_users_token(client):
    auth_string = "test1:FlaskIsAwesome"
    encoded_auth_string = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    headers = {"Authorization": f"Basic {encoded_auth_string}"}
    response = client.get(TOKEN_ENDPOINT, headers=headers)
    assert response.status_code == 200
    assert response.json["token"] is not None
    assert response.json["duration"] == 600