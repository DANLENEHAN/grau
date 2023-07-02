from datetime import datetime

from freezegun import freeze_time
from freezegun.api import FakeDatetime

from grau.db.user.user_model import User, UserValidationSchema
from grau.utils import decrypt_str


class TestUserModel:
    """
    Testing the user validation schema and
    user model
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
        "premium": True,
        "username": "danlen97",
        "weight_unit_pref": "kg",
    }

    @freeze_time("2023-01-01 12:00:00")
    def test_validate_valid_user(self, db_session):
        """
        Tests the user validation schema with a valid user
        object
        """

        # validating and defaulting user schema
        user_object = UserValidationSchema(**self.user_object)
        # create user object
        user = User(**user_object.dict())
        # if invalid fields passed an exception will be raised
        db_session.add(user)
        db_session.commit()

        # static fields: should be the same as the original
        for attribute, value in self.user_object.items():
            if attribute not in ["password", "birthday"]:
                assert getattr(user, attribute) == value

        # API defined or transformed fields: different
        # or not included in original obj
        assert user.id == 1
        assert decrypt_str(user.password) == self.user_object["password"]
        assert user.birthday == datetime(1997, 5, 18, 0, 0)
        assert user.status == "active"

        assert user.created_at == FakeDatetime(2023, 6, 27, 17, 4, 42, 139677)
        assert user.updated_at == FakeDatetime(2023, 6, 27, 17, 4, 42, 139677)
        assert (user.session_id and user.profile_link) is None
