from grau.blueprints.user.functions import get_user
from grau.utils import decrypt_str

SAMPLE_USER = {
    "fullname": "dan lenehan",
    "email": "dan@gmail.com",
    "password": "testing123",
    "status": "active",
}


def test_insert_user(db_session, client):
    """
    Tests the create_user function in grau/blueprints/user/functions.py
    """

    response = client.post("/create_user", json=SAMPLE_USER)
    assert response.status_code == 201
    assert response.data == b"User created successfully"

    user = get_user(db_session, SAMPLE_USER["email"])
    assert user.fullname == SAMPLE_USER["fullname"]
    assert user.email == SAMPLE_USER["email"]
    assert decrypt_str(user.password) == SAMPLE_USER["password"]
    assert user.status == SAMPLE_USER["status"]


def test_login_user(client):
    """
    Tests the login endpoint in grau/blueprints/user/functions.py
    This test is dependent on test_insert_user
    """
    response = client.post(
        "/login",
        json={"email": SAMPLE_USER["email"], "password": SAMPLE_USER["password"]},
    )
    assert response.status_code == 200
    assert response.data == b"Login successful"


def test_user_auth(client):
    """
    Tests the user_authenticated endpoint in grau/blueprints/user/functions.py
    This test is dependent on test_insert_user
    """
    response = client.get("/user_authenticated")
    assert response.status_code == 200
    assert response.data == b"User Authenticated"


def test_logout_user(client):
    """
    Tests the logout endpoint in grau/blueprints/user/functions.py
    This test is dependent on test_insert_user
    """
    response = client.post("/logout", json={"session_id": "testing123"})
    assert response.status_code == 200
    assert response.data == b"Logout successful"


def test_user_auth_logged_out_user(client):
    """
    Tests the user_authenticated endpoint in grau/blueprints/user/functions.py
    This test is dependent on test_insert_user
    """
    response = client.get("/user_authenticated")
    assert response.status_code == 401
