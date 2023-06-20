import datetime as dt

import pytest

from grau.blueprints.user_stats import functions


class TestFunctions:
    """
    Test functions for user_stats.
    """

    @pytest.mark.usefixtures(
        "db_session", "frozen_datetime", "insert_user_stat"
    )
    @pytest.mark.parametrize(
        "user_id, expected_value, user_stat_id, stat_unit", [(1, 100, 1, "kg")]
    )
    def test_get_user_stats(  # noqa pylint: disable=R0913
        self,
        db_session,
        user_id,
        expected_value,
        user_stat_id,
        stat_unit,
    ):
        """
        Test get_user_stats function.
        """
        # Given
        # When
        result = functions.get_user_stat(db_session, user_id, user_stat_id)

        # Then
        assert (
            result.value == expected_value
            and result.id == user_stat_id
            and result.user_id == user_id
            and result.unit == stat_unit
            and result.created_at == dt.datetime(2023, 1, 1)
            and result.updated_at == dt.datetime(2023, 1, 1)
        )
