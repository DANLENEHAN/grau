from grau.db.model import User

"""
Testing ToDos:
	Mock flask API
"""


def test_insert_user(db_session):
    db_session.add(
        User(
            **{
                "fullname": "dan lenehan",
                "email": "dan@gmail.com",
                "password": "testing123",
            }
        )
    )
    db_session.commit()

    user = db_session.query(User).one()

    assert user.fullname == "dan lenehan"
    assert user.email == "dan@gmail.com"
    assert user.password == "testing123"
