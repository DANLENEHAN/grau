"""
Integration scenarios testing user login, logout
and session handling capabilities
"""


class TestUserSessionIntegration:
    """
    Class to test user login, logout and session handling
    """

    user_object = {
        "age": 25,
        "area_code": "353",
        "birthday": "1997-05-18",
        "date_format_pref": "%d-%m-%Y",
        "email": "dan@trainai.com",
        "first_name": "Dan",
        "gender": "male",
        "height_unit_pref": "cm",
        "language": "english",
        "last_name": "lenehan",
        "password": "testing123",
        "phone_number": "6307731531",
        "username": "danlen97",
        "weight_unit_pref": "kg",
    }

    def test_insert_user(self, module_client):
        """
        Tests the create_user function in grau/blueprints/user/functions.py
        """

        response = module_client.post("/create_user", json=self.user_object)
        assert response.status_code == 201
        assert response.data == b"User created successfully"

    def test_login_user(self, module_client):
        """
        Tests the login endpoint in grau/blueprints/user/functions.py
        This test is dependent on test_insert_user
        """
        response = module_client.post(
            "/login",
            json={
                "email": self.user_object["email"],
                "password": self.user_object["password"],
            },
        )
        assert response.status_code == 200
        assert response.data == b"Login successful"

    def test_user_auth(self, module_client):
        """
        Tests the user_authenticated
            (endpoint in grau/blueprints/user/functions.py)
        This test is dependent on test_insert_user
        """
        response = module_client.get("/user_authenticated")
        assert response.status_code == 200
        assert response.data == b"User Authenticated"

    def test_logout_user(self, module_client):
        """
        Tests the logout endpoint in grau/blueprints/user/functions.py
        This test is dependent on test_insert_user
        """
        response = module_client.post(
            "/logout", json={"session_id": "testing123"}
        )
        assert response.status_code == 200
        assert response.data == b"Logout successful"

    def test_user_auth_logged_out_user(self, module_client):
        """
        Tests the user_authenticated
            (endpoint in grau/blueprints/user/functions.py)
        This test is dependent on test_insert_user
        """
        response = module_client.get("/user_authenticated")
        assert response.status_code == 401
