def test_app_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"You've reached the resistance."


def test_app_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_app_test_db(client):
    response = client.get("/test_db")
    assert response.status_code == 200
    assert response.data == b"ok"
