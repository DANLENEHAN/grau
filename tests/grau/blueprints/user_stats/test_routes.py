import datetime as dt
from typing import Dict
from unittest.mock import ANY, MagicMock, patch

from grau.utils import decrypt_str


class UserFactory:
    """
    Factory for creating users.
    """

    def __init__(self):
        self.current_id: int = 1

    def get_user(self, **kwargs) -> Dict:
        """
        Returns a user dictionary.
        """
        user_id = self.current_id
        self.current_id += 1
        user = {
            "id": user_id,
            "username": "test_user",
            "email": "test_email",
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
        user.update(kwargs)
        return user


class UserStatsFactory:
    """
    Factory for creating user stats.
    """

    def __init__(self):
        self.current_id: int = 1

    def get_user_stats(self, user_id: int, **kwargs) -> Dict:
        """
        Returns a user stats dictionary.
        """
        id_ = self.current_id
        self.current_id += 1
        stat = {
            "id": id_,
            "user_id": user_id,
            "value": 1,
            "unit": "kg",
            "note": "this note is a nice note",
        }
        stat.update(kwargs)
        return stat


class TestRoutes:
    """
    Test routes for user_stats.
    """

    user_factory = UserFactory()
    user_stat_factory = UserStatsFactory()

    @patch("grau.blueprints.user_stats.routes.functions.create_user_stats")
    def test_create_user_stats(
        self,
        mock_create_user_stats: MagicMock,
        client,
        insert_user,
        login_user,
    ):
        """
        Test create_user_stats route.
        """
        # Given
        test_user = self.user_factory.get_user()
        test_user_stat = self.user_stat_factory.get_user_stats(
            user_id=test_user["id"]
        )
        user = insert_user(test_user)
        login_user(user)

        # When
        client.post(
            "/create_user_stats",
            json={"user_stats_dict": test_user_stat.copy()},
            follow_redirects=True,
        )
        # Then
        mock_create_user_stats.assert_called_once_with(
            db_session=ANY, user_stats_dict=test_user_stat
        )

    def test_create_user_stats_no_login(self, client):
        """
        Test create_user_stats route.
        """
        # Given

        test_user_stat = self.user_stat_factory.get_user_stats(
            user_id=99999999
        )

        # When
        response = client.post(
            "/create_user_stats",
            json={"user_stats_dict": test_user_stat.copy()},
            follow_redirects=True,
        )
        # Then
        assert (
            response.status_code == 401
            and response.status == "401 UNAUTHORIZED"
        )

    @patch("grau.blueprints.user_stats.routes.functions.delete_user_stat")
    def test_delete_user_stats(
        self,
        mock_delete_user_stat: MagicMock,
        client,
        insert_user,
        login_user,
        insert_user_stat,
    ):
        # Given
        test_user = insert_user(self.user_factory.get_user())
        test_user_stat = insert_user_stat(
            self.user_stat_factory.get_user_stats(user_id=test_user["id"])
        )
        login_user(test_user)
        # When
        client.delete(
            "/delete_user_stat",
            json={"user_stats_dict": test_user_stat.copy()},
        )
        # Then
        mock_delete_user_stat.assert_called_once_with(
            db_session=ANY,
            user_id=test_user["id"],
            stat_id=test_user_stat["id"],
        )

    @patch(
        "grau.blueprints.user_stats.routes.functions.update_user_stat",
        side_effect=lambda db_session, user_stats_dict: user_stats_dict,
    )
    def test_update_user_stat(
        self,
        mock_update_user_stat: MagicMock,
        client,
        insert_user,
        login_user,
        insert_user_stat,
    ):
        # Given
        test_user = insert_user(self.user_factory.get_user())
        test_user_stat = insert_user_stat(
            self.user_stat_factory.get_user_stats(user_id=test_user["id"])
        )
        login_user(test_user)

        updated_user_stat = test_user_stat.copy()
        updated_user_stat["value"] = 2
        updated_user_stat["unit"] = "lbs"

        # When
        result = client.put(
            "/update_user_stat",
            json={"user_stats_dict": updated_user_stat.copy()},
        )
        # Then
        for field in updated_user_stat:
            if field not in ["created_at", "updated_at"]:
                assert result.json[field] == updated_user_stat[field]

    @patch("grau.blueprints.user_stats.routes.functions.get_user_stats")
    def test_get_user_stats(
        self,
        mock_get_user_stats: MagicMock,
        client,
        insert_user,
        login_user,
        insert_user_stat,
    ):
        # Given
        test_user = insert_user(self.user_factory.get_user())
        login_user(test_user)

        # When
        mock_get_user_stats(db_session=ANY, user_id=test_user["id"])
