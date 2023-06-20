import datetime as dt

from grau.blueprints.user.functions import get_user

SAMPLE_USER = {
    "username": "test_user",
    "email": "test@email.com",
    "password": "test_password",
    "session_id": "test_session_id",
    "status": "active",
    "profile_link": "test_profile_link",
    "premium": False,
    "age": 21,
    "birthday": dt.date(2000, 1, 1).strftime("%Y-%m-%d"),
    "first_name": "dan",
    "last_name": "test",
    "gender": "male",
    "phone_number": "1234567890",
    "area_code": "123",
    "height_unit_pref": "cm",
    "weight_unit_pref": "lbs",
    "date_format_pref": "YYYY-MM-DD",
    "language": "en",
}


def test_insert_user(db_session, client):
    """
    Tests the create_user function in grau/blueprints/user/functions.py
    """

    response = client.post("/create_user", json=SAMPLE_USER)
    assert response.status_code == 201
    assert response.data == b"User created successfully"
    # assert that the user was inserted into the database
    user = get_user(db_session, SAMPLE_USER["email"])
    assert user.username == SAMPLE_USER["username"]


def test_login_user(client):
    """
    Tests the login endpoint in grau/blueprints/user/functions.py
    This test is dependent on test_insert_user
    """
    response = client.post(
        "/login",
        json={
            "email": SAMPLE_USER["email"],
            "password": SAMPLE_USER["password"],
        },
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
