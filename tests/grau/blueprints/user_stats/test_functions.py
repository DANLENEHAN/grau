from typing import Dict

import pytest

from grau.blueprints.user_stats import functions


class TestFunctions:
    """
    Test functions for user_stats.
    """

    user_stat: Dict = {
        "id": 1,
        "user_id": 1,
        "value": 1,
        "unit": "kg",
        "note": "this note is a nice note",
    }
    user_id_no_stats: int = 404

    @pytest.mark.usefixtures("frozen_datetime")
    def test_get_user_stat(self, function_db_session, insert_user_stat):
        """
        Test get_user_stats function.
        """
        # Given
        user_stat = self.user_stat.copy()
        user_stat["id"] = 1
        insert_user_stat(user_stat)

        # When
        result = functions.get_user_stat(
            function_db_session,
            user_id=user_stat["user_id"],
            stat_id=user_stat["id"],
        )
        # then
        for key in user_stat:  # noqa: pylint ignore=C0206
            assert result.__dict__[key] == user_stat[key]

    @pytest.mark.usefixtures("frozen_datetime")
    def test_update_user_stat(self, function_db_session, insert_user_stat):
        """
        Test update_user_stat function.
        """
        # Given
        user_stat = self.user_stat.copy()
        user_stat["id"] = 2
        insert_user_stat(user_stat)
        new_user_stat = user_stat.copy()
        new_user_stat["value"] = 2
        new_user_stat["unit"] = "lbs"

        # When
        request_response = functions.update_user_stat(
            function_db_session, new_user_stat
        )
        result = functions.get_user_stat(
            function_db_session,
            user_id=user_stat["user_id"],
            stat_id=user_stat["id"],
        )
        # then
        assert request_response == ("User stat updated successfully", 200)
        for key in user_stat:
            assert result.__dict__[key] == new_user_stat[key]

    @pytest.mark.usefixtures("frozen_datetime")
    def test_get_user_stats(self, function_db_session, insert_user_stat):
        """
        Test get_user_statss function.
        """
        # Given
        user_stat = self.user_stat.copy()
        user_stat["id"] = 3
        user_stat["user_id"] = 2
        new_user_stat = {
            "id": 4,
            "user_id": 2,
            "value": 2,
            "unit": "kg",
            "note": "this note is another nice note",
        }
        insert_user_stat(user_stat)
        insert_user_stat(new_user_stat)

        # When
        stat_result_a, stat_result_b = functions.get_user_stats(
            function_db_session, user_id=user_stat["user_id"]
        )
        # then
        for key in user_stat:
            assert stat_result_a.__dict__[key] == user_stat[key]
            assert stat_result_b.__dict__[key] == new_user_stat[key]

    @pytest.mark.usefixtures("frozen_datetime")
    def test_delete_user_stat(self, function_db_session, insert_user_stat):
        """
        Test delete_user_stat function.
        """
        # Given
        user_stat = self.user_stat.copy()
        user_stat["id"] = 5
        insert_user_stat(user_stat)

        # When
        functions.delete_user_stat(
            function_db_session,
            user_id=user_stat["user_id"],
            stat_id=user_stat["id"],
        )
        result = functions.get_user_stat(
            function_db_session,
            user_id=user_stat["user_id"],
            stat_id=user_stat["id"],
        )
        # then
        assert result is None

    @pytest.mark.usefixtures("frozen_datetime")
    def test_get_user_stat_no_stat(self, function_db_session):
        """
        Test get_user_stats function.
        """
        # Given
        # When
        result = functions.get_user_stat(
            function_db_session,
            user_id=self.user_id_no_stats,
            stat_id=self.user_id_no_stats,
        )
        # then
        assert result is None

    @pytest.mark.usefixtures("frozen_datetime")
    def test_update_user_stat_no_stat(self, function_db_session):
        """
        Test update_user_stat function.
        """
        # Given
        user_stat = self.user_stat.copy()
        user_stat["user_id"] = self.user_id_no_stats
        # When
        request_response = functions.update_user_stat(
            function_db_session, user_stat
        )
        # then
        assert request_response == ("User stat not found", 404)

    @pytest.mark.usefixtures("frozen_datetime")
    def test_get_user_stats_no_stats(self, function_db_session):
        """
        Test get_user_statss function.
        """
        # Given
        self.user_stat.copy()

        # When
        result = functions.get_user_stats(
            function_db_session, user_id=self.user_id_no_stats
        )
        # then
        assert len(result) == 0

    @pytest.mark.usefixtures("frozen_datetime")
    def test_delete_user_stat_no_stat(self, function_db_session):
        """
        Test delete_user_stat function.
        """
        # Given
        self.user_stat.copy()

        # When
        result = functions.delete_user_stat(
            function_db_session,
            user_id=self.user_id_no_stats,
            stat_id=self.user_id_no_stats,
        )

        # then
        assert result == ("User stat not found", 404)
