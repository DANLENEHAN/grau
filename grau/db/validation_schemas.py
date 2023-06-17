from marshmallow import Schema, ValidationError, fields, validate, validates


class UserSchema(Schema):
    """
    Schema for validating user data
    """

    email = fields.Email(required=True)
    fullname = fields.Str(required=True, validate=validate.Length(min=9))
    password = fields.Str(required=True, validate=validate.Length(min=8))

    @validates("fullname")
    def validate_fullname(self, value):  # noqa pylint: disable=R0201
        """
        Validates the fullname field
        """
        if not value.replace(" ", "").isalpha():
            raise ValidationError("Full name must contain only letters")
        if len(value.split(" ")) < 2:
            raise ValidationError("Full name must contain first and last name")
