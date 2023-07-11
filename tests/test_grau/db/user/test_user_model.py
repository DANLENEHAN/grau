from datetime import date

from grau.db.user.user_model import User, UserSchema
from grau.utils import decrypt_str


class TestUserModel:
    """
    Testing the user validation schema and
    user model
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

    def test_validate_valid_user(self, db_session):
        """
        Tests the user validation schema with a valid user
        object
        """

        # validating and defaulting user schema
        user_object = UserSchema(**self.user_object)
        # create user object
        user = User(**user_object.dict())
        # if invalid fields passed an exception will be raised
        db_session.add(user)
        db_session.commit()

        # static fields: should be the same as the original
        for attribute, value in self.user_object.items():
            if attribute not in ["password", "birthday", "phone_number"]:
                assert getattr(user, attribute) == value

        # API defined or transformed fields: different
        # or not included in original obj
        assert user.id == 1
        assert decrypt_str(user.password) == self.user_object["password"]
        assert user.birthday == date(1997, 5, 18)
        assert user.status == "active"
        assert user.phone_number == "tel:+44-7308-831531"

        assert isinstance(user.created_at, date)
        assert isinstance(user.updated_at, date)
        assert user.created_at == user.updated_at
        assert (user.session_id and user.profile_link) is None
