from people_api.constants import PEOPLE_ENDPOINT


def test_person_post(client, token_header):
    new_person = {"fname": "David", "lname": "Metcalf"}
    response = client.post(PEOPLE_ENDPOINT, headers=token_header, json=new_person)
    assert response.status_code == 201
    assert response.json["fname"] == "David"
    assert response.json["lname"] == "Metcalf"
    
def test_person_post_duplicate(client, token_header):
    new_person = {"fname": "David", "lname": "Metcalf"}
    response = client.post(PEOPLE_ENDPOINT, headers=token_header, json=new_person)
    assert response.status_code == 406

def test_person_post_incomplete_request_body(client, token_header):
    new_person = {"fname": "David"}
    response = client.post(PEOPLE_ENDPOINT, headers=token_header, json=new_person)
    assert response.status_code == 400

def test_person_post_invalid_request_body(client, token_header):
    new_person = {"fname": "David", "tname": "Tariq"}
    response = client.post(PEOPLE_ENDPOINT, headers=token_header, json=new_person)
    assert response.status_code == 400

def test_person_post_invalid_media_type(client, token_header):
    headers = {"Content-Type": "application/xml"}
    headers.update(token_header)
    new_person = """
    <xml>
        <fname>David</fname>
        <lname>Tariq</lname>
    </xml>
    """
    response = client.post(PEOPLE_ENDPOINT, headers=headers, data=new_person)
    assert response.status_code == 415

def test_get_all_people(client, token_header):
    response = client.get(PEOPLE_ENDPOINT, headers=token_header)
    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_single_person(client, token_header):
    response = client.get(f"{PEOPLE_ENDPOINT}/Metcalf", headers=token_header)
    assert response.status_code == 200
    assert response.json["fname"] == "David"
    assert response.json["lname"] == "Metcalf"

def test_get_single_person_not_found(client, token_header):
    response = client.get(f"{PEOPLE_ENDPOINT}/Tariq", headers=token_header)
    assert response.status_code == 404

def test_update_person(client, token_header):
    update_person = {"fname": "Fatima", "lname": "Metcalf"}
    response = client.put(f"{PEOPLE_ENDPOINT}/Metcalf", headers=token_header, json=update_person)
    assert response.status_code == 200
    assert response.json["fname"] == "Fatima"
    assert response.json["lname"] == "Metcalf"

def test_update_person_incomplete_request(client, token_header):
    update_person = {"fname": "Fatima"}
    response = client.put(f"{PEOPLE_ENDPOINT}/Metcalf", headers=token_header, json=update_person)
    assert response.status_code == 400

def test_update_person_invalid_request(client, token_header):
    update_person = {"fname": "Fatima", "tname": "Metcalf"}
    response = client.put(f"{PEOPLE_ENDPOINT}/Metcalf", headers=token_header, json=update_person)
    assert response.status_code == 400

def test_update_person_not_found(client, token_header):
    update_person = {"fname": "Fatima", "lname": "Tariq"}
    response = client.put(f"{PEOPLE_ENDPOINT}/Tariq", headers=token_header, json=update_person)
    assert response.status_code == 404

def test_delete_person(client, token_header):
    response = client.delete(f"{PEOPLE_ENDPOINT}/Metcalf", headers=token_header)
    assert response.status_code == 204

def test_delete_person_not_found(client, token_header):
    response = client.delete(f"{PEOPLE_ENDPOINT}/Tariq", headers=token_header)
    assert response.status_code == 404