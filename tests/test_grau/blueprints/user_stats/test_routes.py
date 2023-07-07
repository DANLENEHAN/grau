import datetime as dt
from typing import Dict
from unittest.mock import ANY, MagicMock, patch

from freezegun import freeze_time


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
            "email": "test_email@emial.com",
            "password": "test_password",
            "session_id": "test_session_id",
            "status": "active",
            "profile_link": "https://wwww.test.com",
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
            "date_format_pref": "%Y-%m-%d",
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
        test_user_a = self.user_factory.get_user(id=13)
        test_user_stat = self.user_stat_factory.get_user_stats(
            user_id=test_user_a["id"]
        )
        user = insert_user(test_user_a)
        login_user(user)

        # When
        client.post(
            "/create_user_stat",
            json={"user_stat_dict": test_user_stat.copy()},
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
            "/create_user_stat",
            json={"user_stats_dict": test_user_stat.copy()},
            follow_redirects=True,
        )
        # Then
        assert (
            response.status_code == 401
            and response.status == "401 UNAUTHORIZED"
        )

    @patch("grau.blueprints.user_stats.routes.functions.delete_user_stat")
    def test_delete_user_stats(  # noqa pylint: disable=R0913
        self,
        mock_delete_user_stat: MagicMock,
        client,
        insert_user,
        login_user,
        insert_user_stat,
    ):
        """
        Test delete_user_stats route.
        """
        # Given
        test_user = insert_user(self.user_factory.get_user(id=17))
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
    @freeze_time("2021-01-01")
    def test_update_user_stat(  # noqa pylint: disable=R0913
        self,
        mock_update_user_stat: MagicMock,
        client,
        insert_user,
        login_user,
        insert_user_stat,
    ):
        """
        Test update_user_stat route.
        """
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

        client.put(
            "/update_user_stat",
            json={"user_stats_dict": updated_user_stat.copy()},
        )
        # Then
        expected_user_stat = updated_user_stat.copy()
        # TODO: This is a hack to get around the fact that the datetime
        # is beign converted to a string by the json encoder
        expected_user_stat["created_at"] = expected_user_stat[
            "created_at"
        ].strftime("%a, %d %b %Y %H:%M:%S GMT")
        expected_user_stat["updated_at"] = expected_user_stat[
            "updated_at"
        ].strftime("%a, %d %b %Y %H:%M:%S GMT")

        mock_update_user_stat.assert_called_once_with(
            db_session=ANY,
            user_stats_dict=expected_user_stat,
        )

    @patch("grau.blueprints.user_stats.routes.functions.get_user_stats")
    def test_get_user_stats(
        self,
        mock_get_user_stats: MagicMock,
        insert_user,
        login_user,
        client,
    ):
        """
        Test get_user_stats route.
        """
        # Given
        test_user = insert_user(self.user_factory.get_user())
        login_user(test_user)

        # When
        client.get("/get_user_stats", json={"user_id": test_user["id"]})

        # Then
        mock_get_user_stats.assert_called_once_with(
            db_session=ANY, user_id=test_user["id"]
        )
