"""
Integration scenarios testing user login, logout
and session handling capabilities
"""


class TestUserSessionIntegration:
    """
    Tests the user session handling capabilities
    """

    user_object = {
        "age": 25,
        "birthday": "1997-05-18",
        "date_format_pref": "%d-%m-%Y",
        "email": "dan@trainai.com",
        "first_name": "Dan",
        "gender": "male",
        "height_unit_pref": "cm",
        "language": "english",
        "last_name": "lenehan",
        "password": "testing123",
        "phone_number": "+447308831531",
        "premium": True,
        "username": "danlen97",
        "weight_unit_pref": "kg",
    }

    def test_user_session_management(self, client):
        """
        Tests the user session management capabilities
        """

        response = client.post("/create_user", json=self.user_object)
        assert response.status_code == 201
        assert response.data == b"User created successfully"

        response = client.post(
            "/login",
            json={
                "email": self.user_object["email"],
                "password": self.user_object["password"],
            },
        )
        assert response.status_code == 200
        assert response.data == b"Login successful"

        response = client.get("/user_authenticated")
        assert response.status_code == 200
        assert response.data == b"User Authenticated"

        response = client.post("/logout", json={"session_id": "testing123"})
        assert response.status_code == 200
        assert response.data == b"Logout successful"

        response = client.get("/user_authenticated")
        assert response.status_code == 401
