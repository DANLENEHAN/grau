from unittest.mock import ANY, MagicMock, patch

from freezegun import freeze_time


class TestRoutes:
    """
    Test routes for user_stats.
    """

    @patch("grau.blueprints.user_stats.routes.functions.create_user_stats")
    def test_create_user_stats(
        self,
        mock_create_user_stats: MagicMock,
        client,
        insert_user,
        user_stats_factory,
    ):
        """
        Test create_user_stats route.
        """
        # Given
        user = insert_user()
        test_user_stat = user_stats_factory(user_id=user.id)

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

    def test_create_user_stats_no_login(self, client, user_stats_factory):
        """
        Test create_user_stats route.
        """
        # Given

        test_user_stat = user_stats_factory(user_id=1)

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
        insert_user_stat,
        user_stats_factory,
    ):
        """
        Test delete_user_stats route.
        """
        # Given
        test_user = insert_user()
        user_stat = user_stats_factory(user_id=test_user.id)
        test_user_stat = insert_user_stat(user_stat)
        user_stat["id"] = test_user_stat.id

        # When
        client.delete(
            "/delete_user_stat",
            json={"user_stats_dict": user_stat.copy()},
        )
        # Then
        mock_delete_user_stat.assert_called_once_with(
            db_session=ANY,
            user_id=test_user.id,
            stat_id=test_user_stat.id,
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
        user_stats_factory,
        insert_user_stat,
    ):
        """
        Test update_user_stat route.
        """
        # Given
        test_user = insert_user()
        user_stat = user_stats_factory(user_id=test_user.id)
        test_user_stat = insert_user_stat(user_stat)
        user_stat["id"] = test_user_stat.id

        updated_user_stat = user_stat.copy()
        updated_user_stat["value"] = 2
        updated_user_stat["unit"] = "lbs"

        # When

        client.put(
            "/update_user_stat",
            json={"user_stats_dict": updated_user_stat.copy()},
        )
        # Then
        expected_user_stat = updated_user_stat.copy()
        mock_update_user_stat.assert_called_once_with(
            db_session=ANY,
            user_stats_dict=expected_user_stat,
        )

    @patch("grau.blueprints.user_stats.routes.functions.get_user_stats")
    def test_get_user_stats(
        self,
        mock_get_user_stats: MagicMock,
        insert_user,
        client,
    ):
        """
        Test get_user_stats route.
        """
        # Given
        test_user = insert_user()

        # When
        client.get("/get_user_stats", json={"user_id": test_user.id})

        # Then
        mock_get_user_stats.assert_called_once_with(
            db_session=ANY, user_id=test_user.id
        )
