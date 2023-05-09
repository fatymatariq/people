from people_api.constants import NOTES_ENDPOINT, PEOPLE_ENDPOINT


def test_note_post(client, token_header):
    person = {"fname": "David", "lname": "Metcalf"}
    response = client.post(PEOPLE_ENDPOINT, headers=token_header, json=person)
    assert response.status_code == 201

    new_note = {"person_id": 1, "content": "First note."}
    response = client.post(NOTES_ENDPOINT, headers=token_header, json=new_note)

    assert response.status_code == 201
    assert response.json["person_id"] == 1
    assert response.json["content"] == "First note."
    
def test_note_post_duplicate(client, token_header):
    new_note = {"person_id": 1, "content": "Second note."}
    response = client.post(NOTES_ENDPOINT, headers=token_header, json=new_note)

    assert response.status_code == 201
    assert response.json["person_id"] == 1
    assert response.json["content"] == "Second note."

def test_note_post_invalid_person(client, token_header):
    new_note = {"person_id": 15, "content": "Third note."}
    response = client.post(NOTES_ENDPOINT, headers=token_header, json=new_note)
    assert response.status_code == 404

def test_note_post_missing_person(client, token_header):
    new_note = {"content": "Test content."}
    response = client.post(NOTES_ENDPOINT, headers=token_header, json=new_note)
    assert response.status_code == 404

def test_note_post_invalid_media_type(client, token_header):
    headers = {"Content-Type": "application/xml"}
    headers.update(token_header)
    new_note = """
    <xml>
        <note_id>1</note_id>
        <content>Test Content.</content>
    </xml>
    """
    response = client.post(NOTES_ENDPOINT, headers=headers, data=new_note)
    assert response.status_code == 415

def test_person_invalid_request_body(client, token_header):
    new_person = {"person_id": 1, "cnntent": "Test content."}
    response = client.post(PEOPLE_ENDPOINT, headers=token_header, json=new_person)
    assert response.status_code == 400

def test_get_single_note(client, token_header):
    response = client.get(f"{NOTES_ENDPOINT}/1", headers=token_header,)
    assert response.status_code == 200
    assert response.json["content"] == "First note."

def test_get_single_note_not_found(client, token_header):
    response = client.get(f"{NOTES_ENDPOINT}/16", headers=token_header,)
    assert response.status_code == 404

def test_update_note(client, token_header):
    update_note = {"person_id": 1, "content": "Updated first note."}
    response = client.put(f"{NOTES_ENDPOINT}/1", headers=token_header, json=update_note)
    assert response.status_code == 200
    assert response.json["content"] == "Updated first note."

def test_update_note_without_person_id(client, token_header):
    update_note = {"content": "Updated first note again."}
    response = client.put(f"{NOTES_ENDPOINT}/1", headers=token_header, json=update_note)
    assert response.status_code == 200
    assert response.json["content"] == "Updated first note again."

def test_update_note_not_found(client, token_header):
    update_note = {"person_id": 1, "content": "First note."}
    response = client.put(f"{NOTES_ENDPOINT}/16", headers=token_header, json=update_note)
    assert response.status_code == 404

def test_delete_note(client, token_header):
    response = client.delete(f"{NOTES_ENDPOINT}/1", headers=token_header)
    assert response.status_code == 204

def test_delete_note_not_found(client, token_header):
    response = client.delete(f"{NOTES_ENDPOINT}/1", headers=token_header,)
    assert response.status_code == 404