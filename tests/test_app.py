"""
Tests for the app.py file in the root directory.
"""


def test_app_index(function_client):
    """
    Tests the index endpoint in grau/blueprints/index/functions.py
    """
    response = function_client.get("/")
    assert response.status_code == 200
    assert response.data == b"You've reached the resistance."


def test_app_health(function_client):
    """
    Tests the health endpoint in grau/blueprints/health/functions.py
    """
    response = function_client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_app_test_db(function_client):
    """
    Tests the test_db endpoint in grau/blueprints/user/functions.py
    """
    response = function_client.get("/test_db")
    assert response.status_code == 200
    assert response.data == b"ok"
