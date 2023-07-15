import pytest

from grau.blueprints.user_stats import functions


class TestFunctions:
    """
    Test functions for user_stats.
    """

    user_id_no_stats: int = 404

    @pytest.mark.usefixtures("frozen_datetime")
    def test_get_user_stat(self, db_session, insert_user_stat):
        """
        Test get_user_stats function.
        """
        # Given
        user_id = 1
        insert_stat = insert_user_stat(user_id=user_id)

        # When
        result = functions.get_user_stat(
            db_session,
            user_id=user_id,
            stat_id=insert_stat.id,
        )
        # then
        for key, value in insert_stat.__dict__.items():
            assert result.__dict__[key] == value

    @pytest.mark.usefixtures("frozen_datetime")
    def test_update_user_stat(
        self, db_session, insert_user_stat, user_stats_factory
    ):
        """
        Test update_user_stat function.
        """
        # Given
        user_stat = user_stats_factory(user_id=1)
        updated_user_stat = user_stat.copy()
        inserted_user_stat = insert_user_stat(user_stat)
        expected_result = inserted_user_stat.__dict__.copy()

        updated_user_stat["id"] = inserted_user_stat.id
        updated_user_stat["value"] = 2
        updated_user_stat["unit"] = "lbs"

        # When
        request_response = functions.update_user_stat(
            db_session, updated_user_stat
        )
        result = functions.get_user_stat(
            db_session,
            user_id=inserted_user_stat.user_id,
            stat_id=inserted_user_stat.id,
        )
        # then
        assert request_response == ("User stat updated successfully", 200)
        for key, value in expected_result.items():
            if key == "value":
                assert result.__dict__[key] == 2
            elif key == "unit":
                assert result.__dict__[key] == "lbs"
            elif key == "updated_at":
                continue
            else:
                assert result.__dict__[key] == value

    @pytest.mark.usefixtures("frozen_datetime")
    def test_get_user_stats(
        self, db_session, insert_user_stat, user_stats_factory
    ):
        """
        Test get_user_statss function.
        """
        # Given
        user_id = 1
        stats = [
            user_stats_factory(user_id=1, unit="kg"),
            user_stats_factory(user_id=1, unit="lbs"),
        ]
        inserted_stats = [
            insert_user_stat(stats[0]),
            insert_user_stat(stats[1]),
        ]

        # When
        stat_result_a, stat_result_b = functions.get_user_stats(
            db_session, user_id=user_id
        )
        # then
        for key, value in inserted_stats[0].__dict__.items():
            assert stat_result_a.__dict__[key] == value
            assert (
                stat_result_b.__dict__[key] == inserted_stats[1].__dict__[key]
            )

    @pytest.mark.usefixtures("frozen_datetime")
    def test_delete_user_stat(
        self, db_session, insert_user_stat, user_stats_factory
    ):
        """
        Test delete_user_stat function.
        """
        # Given
        inserted_stat = insert_user_stat(user_stats_factory(user_id=1))

        # When
        functions.delete_user_stat(
            db_session,
            user_id=inserted_stat.user_id,
            stat_id=inserted_stat.id,
        )
        result = functions.get_user_stat(
            db_session,
            user_id=inserted_stat.user_id,
            stat_id=inserted_stat.id,
        )
        # then
        assert result is None

    @pytest.mark.usefixtures("frozen_datetime")
    def test_get_user_stat_no_stat(self, db_session):
        """
        Test get_user_stats function.
        """
        # Given
        # When
        result = functions.get_user_stat(
            db_session,
            user_id=self.user_id_no_stats,
            stat_id=self.user_id_no_stats,
        )
        # then
        assert result is None

    @pytest.mark.usefixtures("frozen_datetime")
    def test_update_user_stat_no_stat(self, db_session, user_stats_factory):
        """
        Test update_user_stat function.
        """
        # Given
        user_stat = user_stats_factory(user_id=1)
        user_stat["id"] = self.user_id_no_stats
        # When
        request_response = functions.update_user_stat(db_session, user_stat)
        # then
        assert request_response == ("User stat not found", 404)

    @pytest.mark.usefixtures("frozen_datetime")
    def test_get_user_stats_no_stats(self, db_session):
        """
        Test get_user_statss function.
        """
        # Given

        # When
        result = functions.get_user_stats(
            db_session, user_id=self.user_id_no_stats
        )
        # then
        assert len(result) == 0

    @pytest.mark.usefixtures("frozen_datetime")
    def test_delete_user_stat_no_stat(self, db_session):
        """
        Test delete_user_stat function.
        """
        # Given

        # When
        result = functions.delete_user_stat(
            db_session,
            user_id=self.user_id_no_stats,
            stat_id=self.user_id_no_stats,
        )

        # then
        assert result == ("User stat not found", 404)
